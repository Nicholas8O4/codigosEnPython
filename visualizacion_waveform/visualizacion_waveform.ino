// visualizacion_waveform.ino
// Medición de voltaje/corriente con PLL, cálculo de componentes d-q (Park),
// cálculo de potencias P y Q promediadas cada 168 muestras (~1 ciclo @60Hz),
// selección de sensor de corriente por Serial (1,2,3) con
// reinicio de filtros/PLL al cambiar, y visualización en pantalla OLED SSD1306
// de P, FP, Q y S.
// Versión para ESP32-S3 (sin DAC interno).
// ADC en modo continuo (DMA): el hardware muestrea a tasa fija y la CPU solo procesa.
// DAC externo MCP4725 (0x62, SDA=41, SCL=42): el segundo núcleo visualiza sin(theta) del PLL.
#include <Arduino.h>
#include <Wire.h>
#include <atomic>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_MCP4725.h>

// ---------- Pines (ESP32-S3) ----------
const int PIN_SENSOR   = 6;   // Sensor de corriente (SCT-013)  -> ADC1_CH5 (GPIO6)
const int pinVoltaje   = 5;   // Sensor de voltaje (ZMPT101B)   -> ADC1_CH4 (GPIO5)

// ---------- Identificadores de sensores de corriente ----------
enum SensorCorriente {
  SENSOR_SCT013_10A = 0,
  SENSOR_SCT013_20A = 1,
  SENSOR_SCT013_30A = 2
};

// ---------- Estructura para devolver los dos parámetros juntos ----------
struct CalibracionCorriente {
  float pendiente;
  float intercepto;
};

// ---------- Función que devuelve la calibración según el sensor seleccionado ----------
CalibracionCorriente obtenerCalibracionCorriente(int sensor) {
  CalibracionCorriente cal;

  switch (sensor) {
    case SENSOR_SCT013_10A:
      cal.pendiente  = 0.0668;
      cal.intercepto = 1.772;
      break;

    case SENSOR_SCT013_20A:
      cal.pendiente  = 0.048;   // TODO: reemplazar con la regresión real
      cal.intercepto = 1.773;   // TODO: reemplazar con la regresión real
      break;

    case SENSOR_SCT013_30A:
      cal.pendiente  = 0.0363;  // TODO: reemplazar con la regresión real
      cal.intercepto = 1.772;   // TODO: reemplazar con la regresión real
      break;

    default:
      cal.pendiente  = 0.06387;
      cal.intercepto = 1.772;
      break;
  }

  return cal;
}

// ---------- Selección de sensor en tiempo de ejecución ----------
int sensorActivo = SENSOR_SCT013_10A;              // sensor por defecto al arrancar
CalibracionCorriente calCorriente = obtenerCalibracionCorriente(sensorActivo);

// ---------- Acondicionamiento - Voltaje ----------
const float OFFSET_V = 1.6;
const float FACTOR_V = 100000.0 / (sqrt(2)*1955.0);
const float DIVISOR  = 34.0 / 15.0;

// ---------- Muestreo a periodo fijo (ADC en modo continuo / DMA) ----------
// El ritmo lo marca el reloj del ADC, no micros(): cada 1/FS_HZ el hardware entrega
// una muestra de cada pin, ya promediada sobre CONVERSIONES_POR_PIN lecturas.
const uint32_t FS_HZ = 10080;               // muestras/s por canal -> ~168 muestras/ciclo @60Hz
const uint32_t CONVERSIONES_POR_PIN = 4;    // oversampling por hardware (10080*4*2 = 80640 Hz <= 83333 Hz máx. del S3)
const float Ts = 1.0 / FS_HZ;               // 99.206 us (coincide exacto con FS_HZ)

uint8_t pinesADC[] = { PIN_SENSOR, pinVoltaje };
const int N_PINES_ADC = sizeof(pinesADC) / sizeof(pinesADC[0]);
adc_continuous_result_t *resultadoADC = NULL;   // en core 3.0.x el tipo se llamaba adc_continuous_data_t

volatile unsigned long framesADC = 0;   // muestras completadas por el ADC (lo incrementa la interrupción)
unsigned long framesAtendidos = 0;      // muestras ya procesadas por el loop

// Interrupción: el ADC terminó una muestra (un "frame"). Solo cuenta; el trabajo se hace en loop().
void ARDUINO_ISR_ATTR adcFrameListo() {
  framesADC++;
}

// ---------- Filtro de cuadratura ----------
const float A_QUAD = 0.9630;

// Estado del filtro de cuadratura - VOLTAJE
float coseno_V     = 0;
float coseno_V_ant = 0;
float vFinal_ant   = 0;

// Estado del filtro de cuadratura - CORRIENTE
float coseno_I     = 0;
float coseno_I_ant = 0;
float corriente_ant = 0;

// ---------- Componentes de Park (d-q) ----------
float vd = 0, vq = 0;
float id = 0, iq = 0;
float vd_ant = 0;

// ---------- PLL: controlador PI + integrador de fase ----------
const float PI2 = 2 * 3.1416;
const float w0  = PI2 * 60.0;

const float a1 = 0.10050 * 10;
const float a2 = 0.963;

float pipll     = 0;
float pipll_ant = 0;
float w0p       = w0;
float w0p_ant   = w0;
float theta     = 0;
float theta_ant = 0;

// ---------- Cálculo de potencias P y Q (promedio cada 168 muestras) ----------
const int MUESTRAS_POR_CICLO = 168;  // ~1 ciclo de 60 Hz a ~10080 muestras/s
const float FACTOR_P = 1;            // factor de escala/calibración, ajustar según medición de referencia

float p = 0, q = 0;                  // potencia instantánea
float p_accum = 0, q_accum = 0;      // acumuladores dentro del ciclo actual
int sample_count = 0;
float P_promedio = 0;
float Q_promedio = 0;

// ---------- Corrección de fase de los sensores ----------
// El ZMPT101B y el SCT-013 introducen cada uno un pequeño desfase propio.
// Esta corrección rota el vector (P, Q) para compensarlo.
// Calibración: con una carga PURAMENTE resistiva (bombillo incandescente, plancha, calentador)
// y esta constante en 0, lee P y Q en pantalla y calcula:
//     CORR_FASE_GRADOS = -atan(Q / P) * 180 / pi
// Con el valor correcto, la carga resistiva debe mostrar Q ~ 0 y FP ~ 1.
const float CORR_FASE_GRADOS = 0.0;
const float CORR_COS = cos(CORR_FASE_GRADOS * PI / 180.0);
const float CORR_SIN = sin(CORR_FASE_GRADOS * PI / 180.0);

// ---------- Valores RMS reales (para S y FP verdaderos) ----------
// vFinal y corriente están escalados para que su AMPLITUD sea el valor RMS
// (por eso P = vd*id + vq*iq da watts directamente). El RMS de esas ondas es amplitud/√2,
// así que el RMS real es √2 · rms(onda). Se usa la varianza para quitar el offset DC.
float sv = 0, sv2 = 0;               // suma y suma de cuadrados del voltaje en el ciclo
float si = 0, si2 = 0;               // suma y suma de cuadrados de la corriente en el ciclo
int   n_rms = 0;
float V_real = 0;                    // voltaje RMS verdadero (V)
float I_real = 0;                    // corriente RMS verdadera (A)
int   sensorAnteriorRMS = -1;        // para descartar el ciclo en curso al cambiar de sensor

// =====================================================================
// ---------- DAC MCP4725 en el segundo núcleo ----------
// =====================================================================
// El núcleo de muestreo solo deja sin(theta) en un buffer circular sin bloqueos
// (unas pocas instrucciones por muestra, sin I2C ni FreeRTOS). Una tarea fijada al OTRO
// núcleo lo lee y lo escribe en el DAC por un bus I2C propio (Wire1), así que no compite
// con la OLED (Wire) ni retrasa el muestreo.
const int      DAC_SDA        = 41;       // si SDA/SCL están al revés, intercambia estos dos
const int      DAC_SCL        = 42;
const uint8_t  DAC_DIR        = 0x62;
const uint32_t DAC_I2C_HZ     = 400000;   // máximo del MCP4725 en modo Fast
const int      DAC_DECIMACION = 2;        // 1 de cada N muestras del PLL -> 5040 puntos/s (84 por ciclo)

Adafruit_MCP4725 dac;

// Buffer circular: 1 productor (núcleo de muestreo) y 1 consumidor (núcleo del DAC)
const uint32_t DAC_BUF_N = 256;           // potencia de 2
uint16_t dacBuf[DAC_BUF_N];
std::atomic<uint32_t> dacHead{0};         // lo avanza solo el productor
std::atomic<uint32_t> dacTail{0};         // lo avanza solo el consumidor
volatile uint32_t dacErrores   = 0;       // escrituras I2C fallidas
volatile uint32_t dacDescartes = 0;       // muestras descartadas por buffer lleno
int dacCuenta = 0;                        // contador de decimación (solo núcleo de muestreo)

// Nunca bloquea: si el buffer está lleno, descarta la muestra.
inline void dacPush(uint16_t code) {
  uint32_t h = dacHead.load(std::memory_order_relaxed);
  if (h - dacTail.load(std::memory_order_acquire) >= DAC_BUF_N) { dacDescartes++; return; }
  dacBuf[h & (DAC_BUF_N - 1)] = code;
  dacHead.store(h + 1, std::memory_order_release);
}

// Tarea del DAC (se ejecuta en el núcleo que NO corre loop()).
void tareaDAC(void *) {
  // El bus se inicia AQUÍ para que su interrupción quede en este núcleo
  Wire1.begin(DAC_SDA, DAC_SCL, DAC_I2C_HZ);
  Wire1.setTimeOut(5);
  if (!dac.begin(DAC_DIR, &Wire1)) {
    Serial.println("# DAC MCP4725 no encontrado (0x62, pines 41/42).");
    vTaskDelete(NULL);
  }
  Wire1.setClock(DAC_I2C_HZ);   // begin() puede dejar el reloj por defecto

  uint32_t tail = 0;
  for (;;) {
    uint32_t head = dacHead.load(std::memory_order_acquire);
    uint32_t pendientes = head - tail;
    if (pendientes == 0) continue;                    // nada nuevo: espera activa (este núcleo es solo para esto)
    if (pendientes > DAC_BUF_N / 2) tail = head - 4;  // si se atrasó (p. ej. error de bus), salta a lo reciente

    uint16_t code = dacBuf[tail & (DAC_BUF_N - 1)];
    tail++;
    dacTail.store(tail, std::memory_order_release);

    // Fast mode del MCP4725: [0 0 PD1 PD0 D11..D8][D7..D0]; solo registro del DAC, no EEPROM.
    // (No se usa dac.setVoltage(): reconfigura el reloj I2C dos veces por llamada.)
    Wire1.beginTransmission(DAC_DIR);
    Wire1.write((uint8_t)(code >> 8));
    Wire1.write((uint8_t)(code & 0xFF));
    if (Wire1.endTransmission() != 0) dacErrores++;
  }
}

// ---------- Función para reiniciar el estado de filtros, Park y PLL ----------
// Se debe llamar cada vez que cambia una condición que invalide el estado acumulado
// (ej. cambio de sensor de corriente), para evitar transitorios con datos "viejos".
void reiniciarFiltrosYPLL() {
  // --- Filtro de cuadratura - Corriente ---
  coseno_I      = 0;
  coseno_I_ant  = 0;
  corriente_ant = 0;

  // --- Componentes d-q de corriente ---
  id = 0; iq = 0;

  // --- Potencias y acumuladores ---
  // Se descarta el ciclo en curso: mezclaría muestras con la calibración vieja y la nueva.
  p = 0; q = 0;
  p_accum = 0;
  q_accum = 0;
  sample_count = 0;
  P_promedio = 0;
  Q_promedio = 0;
  Serial.println("# Filtros, Park y PLL reiniciados.");
}

// Revisa si llegó un caracter por Serial y, si es '1', '2' o '3',
// cambia el sensor activo, recalcula su calibración y reinicia filtros/PLL.
// IMPORTANTE: no bloquea, así que es seguro llamarla dentro del loop de muestreo.
void revisarSeleccionSensor() {
  if (Serial.available() > 0) {
    char c = Serial.read();

    int nuevoSensor = -1;
    switch (c) {
      case '1': nuevoSensor = SENSOR_SCT013_10A; break;
      case '2': nuevoSensor = SENSOR_SCT013_20A; break;
      case '3': nuevoSensor = SENSOR_SCT013_30A; break;
      default: break; // ignora cualquier otro caracter (ej. '\n', '\r', espacios)
    }

    if (nuevoSensor != -1 && nuevoSensor != sensorActivo) {
      sensorActivo = nuevoSensor;
      calCorriente = obtenerCalibracionCorriente(sensorActivo);

      reiniciarFiltrosYPLL();   // limpia el estado antes de seguir midiendo

      Serial.print("# Sensor cambiado a: ");
      Serial.print(sensorActivo + 1); // +1 para mostrar 1,2,3 en vez de 0,1,2
      Serial.print(" (pendiente=");
      Serial.print(calCorriente.pendiente, 6);
      Serial.print(", intercepto=");
      Serial.print(calCorriente.intercepto, 4);
      Serial.println(")");
    }
  }
}

// ---------- Función separada del loop ----------
// Recibe los milivoltios ya leídos (y promediados) por el ADC continuo.
// IMPORTANTE: no imprimir por Serial aquí; se ejecuta 10080 veces por segundo
// y cualquier impresión desborda el buffer del ADC.
void muestrearYEnviar(float milivoltios_I, float milivoltios_V) {
  // --- Corriente ---
  float voltaje_I = milivoltios_I / 1000.0;
  float corriente = ((voltaje_I - calCorriente.intercepto) / calCorriente.pendiente) / sqrtf(2);

  // --- Voltaje ---
  float voltajeADC_V = milivoltios_V / 1000.0;
  float vSinOffset = DIVISOR * (voltajeADC_V - OFFSET_V);
  float vFinal = vSinOffset * FACTOR_V;

  // --- Cuadratura de voltaje ---
  coseno_V = coseno_V_ant * A_QUAD - A_QUAD * vFinal + vFinal_ant;

  // --- Cuadratura de corriente ---
  coseno_I = coseno_I_ant * A_QUAD - A_QUAD * corriente + corriente_ant;

  // --- Transformada de Park (d-q), usando el ángulo estimado por el PLL ---
  //vd =  vFinal * cos(theta) + coseno_V * sin(theta);
  //vq = -vFinal * sin(theta) + coseno_V * cos(theta);
  //id =  corriente * cos(theta) + coseno_I * sin(theta);
  //iq = -corriente * sin(theta) + coseno_I * cos(theta);
  float s = sinf(theta);
  float c = cosf(theta);

  // --- Publicar la señal del PLL para el DAC (el núcleo secundario la visualiza) ---
  if (++dacCuenta >= DAC_DECIMACION) {
    dacCuenta = 0;
    dacPush((uint16_t)(2047.5f + 2047.0f * s));   // sin(theta) -> 0..4094, centrado en 2047
  }

  vd =  vFinal * c + coseno_V * s;
  vq = -vFinal * s + coseno_V * c;
  id =  corriente * c + coseno_I * s;
  iq = -corriente * s + coseno_I * c;

  // --- PLL: controlador PI usando vd como señal de error ---
  pipll = pipll_ant + a1 * vd - vd_ant * a2;
  w0p = pipll + w0;

  // --- Integración de fase ---
  theta = w0p_ant * Ts + theta_ant;
  if (theta >= PI2) {
    theta -= PI2;
  }

  // --- Cálculo de potencia instantánea (marco d-q) ---
  p = (vd * id + vq * iq) * FACTOR_P;
  q = (vq * id - vd * iq);

  // --- Acumulación y promedio cada 168 muestras ---
  p_accum += p;
  q_accum += q;
  sample_count++;

  if (sample_count >= MUESTRAS_POR_CICLO) {
    P_promedio = p_accum / MUESTRAS_POR_CICLO;
    Q_promedio = q_accum / MUESTRAS_POR_CICLO;
    p_accum = 0;
    q_accum = 0;
    sample_count = 0;
  }

  // --- Actualizar estado (memoria de filtros e integradores) ---
  coseno_V_ant  = coseno_V;
  vFinal_ant    = vFinal;
  coseno_I_ant  = coseno_I;
  corriente_ant = corriente;

  pipll_ant = pipll;
  vd_ant    = vd;
  w0p_ant   = w0p;
  theta_ant = theta;
}

// Acumula las ondas de voltaje y corriente para calcular su RMS verdadero cada ciclo.
// Se llama justo después de muestrearYEnviar(): vFinal_ant y corriente_ant
// contienen la muestra recién procesada.
void acumularRMS() {
  // Si cambió el sensor, se descarta el ciclo en curso (igual criterio que P y Q)
  if (sensorActivo != sensorAnteriorRMS) {
    sensorAnteriorRMS = sensorActivo;
    sv = 0; sv2 = 0;
    si = 0; si2 = 0;
    n_rms = 0;
    I_real = 0;
  }

  float v = vFinal_ant;
  float i = corriente_ant;
  sv += v;  sv2 += v * v;
  si += i;  si2 += i * i;
  n_rms++;

  if (n_rms >= MUESTRAS_POR_CICLO) {
    float mv = sv / n_rms;                      // offset DC del voltaje
    float mi = si / n_rms;                      // offset DC de la corriente
    float var_v = sv2 / n_rms - mv * mv;        // varianza = RMS^2 sin componente DC
    float var_i = si2 / n_rms - mi * mi;
    if (var_v < 0) var_v = 0;
    if (var_i < 0) var_i = 0;
    V_real = sqrtf(2.0f * var_v);               // √2 · rms(onda) -> RMS real
    I_real = sqrtf(2.0f * var_i);

    sv = 0; sv2 = 0;
    si = 0; si2 = 0;
    n_rms = 0;
  }
}

// =====================================================================
// ---------- Pantalla OLED SSD1306 128x64 (I2C) ----------
// =====================================================================
// La pantalla NO se actualiza con oled.display() dentro del loop, porque enviar
// los 1024 bytes de una vez bloquea varios ms y rompería el muestreo y el PLL.
// En su lugar se usa una máquina de estados no bloqueante que, en cada paso, hace
// un trabajo pequeño: dibujar una línea en RAM o enviar un tramo corto de bytes.
// Muestra: P (W), FP, Q (VAR) y S (VA).

// ---------- Configuración ----------
const int      OLED_SDA    = 9;
const int      OLED_SCL    = 8;
const uint8_t  OLED_DIR    = 0x3C;     // algunas pantallas usan 0x3D
const int      OLED_ANCHO  = 128;
const int      OLED_ALTO   = 64;
const uint32_t OLED_I2C_HZ = 800000;   // 400000 es lo más seguro; la SSD1306 suele aguantar 800k-1M

const unsigned long OLED_PERIODO_MS           = 1000;  // cada cuánto se refresca la pantalla (ms)
const int           OLED_BYTES_POR_TRAMO      = 4;     // bytes de imagen por paso (pequeño: el buffer del ADC guarda solo 2 muestras)
const int           OLED_MUESTRAS_ENTRE_PASOS = 4;     // un paso de pantalla cada N muestras
const float         OLED_S_MINIMA             = 1.0;   // VA; por debajo de esto el FP no se calcula (se muestra "--")

Adafruit_SSD1306 oled(OLED_ANCHO, OLED_ALTO, &Wire, -1, OLED_I2C_HZ, OLED_I2C_HZ);
bool oledOK = false;

// ---------- Máquina de estados de la pantalla ----------
enum EstadoOLED { OLED_ESPERANDO, OLED_DIBUJANDO, OLED_VENTANA, OLED_ENVIANDO };
EstadoOLED estadoOLED = OLED_ESPERANDO;
int lineaOLED = 0;
int indiceBufferOLED = 0;
int contadorPasosOLED = 0;
unsigned long tUltimoRefrescoOLED = 0;

// "Foto" de los valores al iniciar cada refresco, para que las 4 líneas sean coherentes
float P_pant = 0;      // potencia activa (W)
float Q_pant = 0;      // potencia reactiva de 60 Hz (VAR)
float S_pant = 0;      // potencia aparente verdadera (VA) = Vrms · Irms
float FP_pant = 0;     // factor de potencia verdadero = P / S
bool  FP_valido = false;

// Dibuja UNA línea en el buffer de RAM (no envía nada por I2C).
// Texto tamaño 2: 12x16 px por caracter -> 10 caracteres x 4 líneas en 128x64.
void dibujarLineaOLED(int linea) {
  char txt[12];
  switch (linea) {
    case 0: snprintf(txt, sizeof(txt), "P %7.1fW", P_pant); break;    // ej: "P   125.3W"
    case 1:
      if (FP_valido) snprintf(txt, sizeof(txt), "FP %6.3f", FP_pant);  // ej: "FP  0.980"
      else           snprintf(txt, sizeof(txt), "FP     --");          // sin carga: no se calcula
      break;
    case 2: snprintf(txt, sizeof(txt), "Q%6.1fVAR", Q_pant); break;    // ej: "Q  21.4VAR"
    case 3: snprintf(txt, sizeof(txt), "S %6.1fVA", S_pant); break;    // ej: "S  127.1VA"
    default: return;
  }
  oled.setCursor(0, linea * 16);
  oled.print(txt);
}

// Avanza la máquina de estados un paso pequeño. NO bloquea más que un tramo I2C.
void servicioOLED() {
  if (!oledOK) return;

  // Solo se trabaja cada OLED_MUESTRAS_ENTRE_PASOS muestras, para repartir la carga
  if (++contadorPasosOLED < OLED_MUESTRAS_ENTRE_PASOS) return;
  contadorPasosOLED = 0;

  switch (estadoOLED) {

    case OLED_ESPERANDO:
      if (millis() - tUltimoRefrescoOLED >= OLED_PERIODO_MS) {
        tUltimoRefrescoOLED = millis();

        // P y Q con la corrección de fase de los sensores (rotación del vector P-Q)
        P_pant = P_promedio * CORR_COS - Q_promedio * CORR_SIN;
        Q_pant = P_promedio * CORR_SIN + Q_promedio * CORR_COS;

        // S verdadera = Vrms · Irms reales (incluye armónicos, igual que un analizador de redes)
        S_pant = V_real * I_real;

        // FP verdadero = P / S
        FP_valido = (S_pant >= OLED_S_MINIMA);
        FP_pant = FP_valido ? (P_pant / S_pant) : 0;

        oled.clearDisplay();   // solo borra el buffer en RAM
        lineaOLED = 0;
        estadoOLED = OLED_DIBUJANDO;
      }
      break;

    case OLED_DIBUJANDO:
      dibujarLineaOLED(lineaOLED);
      lineaOLED++;
      if (lineaOLED >= 4) {
        estadoOLED = OLED_VENTANA;
      }
      break;

    case OLED_VENTANA: {
      // Ventana completa: columnas 0..127, páginas 0..7 (modo horizontal, lo deja así oled.begin())
      const uint8_t cmds[] = {
        0x00,                                   // byte de control: siguen comandos
        0x21, 0, (uint8_t)(OLED_ANCHO - 1),     // rango de columnas
        0x22, 0, (uint8_t)(OLED_ALTO / 8 - 1)   // rango de páginas
      };
      Wire.beginTransmission(OLED_DIR);
      Wire.write(cmds, sizeof(cmds));
      Wire.endTransmission();
      indiceBufferOLED = 0;
      estadoOLED = OLED_ENVIANDO;
      break;
    }

    case OLED_ENVIANDO: {
      uint8_t *buf = oled.getBuffer();
      const int total = OLED_ANCHO * OLED_ALTO / 8;   // 1024 bytes
      int restantes = total - indiceBufferOLED;
      int n = (restantes < OLED_BYTES_POR_TRAMO) ? restantes : OLED_BYTES_POR_TRAMO;

      Wire.beginTransmission(OLED_DIR);
      Wire.write((uint8_t)0x40);                      // byte de control: siguen datos
      Wire.write(buf + indiceBufferOLED, n);
      Wire.endTransmission();

      indiceBufferOLED += n;
      if (indiceBufferOLED >= total) {
        estadoOLED = OLED_ESPERANDO;                  // refresco terminado
      }
      break;
    }
  }
}

void setup() {
  Serial.begin(921600);

  // ---------- Pantalla OLED ----------
  // Va ANTES de arrancar el ADC, porque la inicialización bloquea varios ms.
  Wire.begin(OLED_SDA, OLED_SCL);
  Wire.setClock(OLED_I2C_HZ);
  Wire.setTimeOut(5);   // ms; si la pantalla se desconecta, no bloquea 50 ms por defecto

  oledOK = oled.begin(SSD1306_SWITCHCAPVCC, OLED_DIR, true, false); // false: Wire ya iniciado arriba
  if (oledOK) {
    Wire.setClock(OLED_I2C_HZ);
    oled.setTextSize(2);
    oled.setTextColor(SSD1306_WHITE);
    oled.setTextWrap(false);
    oled.clearDisplay();
    oled.setCursor(0, 24);
    oled.print("Iniciando");
    oled.display();     // aquí sí se puede bloquear: el muestreo aún no arranca
  } else {
    Serial.println("# OLED no encontrada (revisa direccion 0x3C/0x3D y cableado).");
  }

  // ---------- DAC en el otro núcleo (el que NO ejecuta loop()) ----------
  // setup() corre en loopTask, así que 1 - xPortGetCoreID() es el núcleo contrario.
  xTaskCreatePinnedToCore(tareaDAC, "dac", 4096, NULL, 1, NULL, 1 - xPortGetCoreID());

  // ---------- ADC en modo continuo (DMA) ----------
  // Resolución 12 bits y atenuación 11 dB -> mismos mV calibrados que con analogReadMilliVolts().
  analogContinuousSetWidth(12);
  analogContinuousSetAtten(ADC_11db);

  uint32_t frecConversiones = FS_HZ * CONVERSIONES_POR_PIN * N_PINES_ADC;   // 80640 Hz
  if (!analogContinuous(pinesADC, N_PINES_ADC, CONVERSIONES_POR_PIN, frecConversiones, &adcFrameListo)) {
    Serial.println("# ERROR: no se pudo configurar el ADC continuo.");
    while (true) { delay(1000); }
  }
  analogContinuousStart();
}

void loop() {
  revisarSeleccionSensor();   // revisa cambio de sensor sin bloquear el muestreo

  // --- Procesar todas las muestras que el ADC haya completado ---
  // No hay busy-wait: el ritmo lo marca el reloj del ADC (FS_HZ).
  while (framesAtendidos != framesADC) {
    framesAtendidos++;

    if (!analogContinuousRead(&resultadoADC, 0)) {
      continue;   // el buffer del ADC se desbordó: esa muestra ya no está
    }

    // Buscar cada pin en el resultado (no se asume el orden)
    float mv_I = 0, mv_V = 0;
    for (int k = 0; k < N_PINES_ADC; k++) {
      if (resultadoADC[k].pin == PIN_SENSOR)      mv_I = resultadoADC[k].avg_read_mvolts;
      else if (resultadoADC[k].pin == pinVoltaje) mv_V = resultadoADC[k].avg_read_mvolts;
    }

    muestrearYEnviar(mv_I, mv_V);
    acumularRMS();            // RMS verdadero de V e I (para S y FP)

    // --- Pantalla OLED (no bloqueante, mismo núcleo) ---
    servicioOLED();           // un paso pequeño de la pantalla cada OLED_MUESTRAS_ENTRE_PASOS muestras
  }
    // --- DIAGNÓSTICO TEMPORAL: 1 línea por segundo (quitar al terminar la calibración) ---
  // static unsigned long tDiag = 0;
  // if (millis() - tDiag >= 1000) {
  //   tDiag = millis();
  //   float V_dq = sqrtf(vd * vd + vq * vq);   // V de 60 Hz (método d-q)
  //   float I_dq = sqrtf(id * id + iq * iq);   // I de 60 Hz (método d-q)
  //   Serial.printf("V_real=%.1f V_dq=%.1f | I_real=%.3f I_dq=%.3f | P=%.1f Q=%.1f S=%.1f FP=%.3f | f=%.2f | dacErr=%lu dacDesc=%lu\n",
  //                 V_real, V_dq, I_real, I_dq, P_pant, Q_pant, S_pant, FP_pant, w0p / PI2,
  //                 (unsigned long)dacErrores, (unsigned long)dacDescartes);
  // }
}
