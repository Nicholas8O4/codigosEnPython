% ENTRENARCRIMENGA  Entrenamiento genetico en paralelo de un clasificador de
% criminalidad ALTA / BAJA a partir de:
%     PctDivorcio, PctEmpleo, PctSinSecundaria, PctPobreza
%
% Funcionamiento:
%   1. Cada RONDA lanza una tarea de entrenamiento por nucleo (parfor).
%   2. Cada tarea permuta los datos al azar (70% entrenamiento, 20%
%      validacion, 10% prueba), parte de una poblacion aleatoria y recibe al
%      ultimo mejor individuo para conservar sus caracteristicas.
%   3. Al terminar la ronda se elige al campeon entre las tareas y el campeon
%      anterior, y se repite hasta alcanzar la meta o agotar la paciencia.
%
% Sobre "predecir el proximo mes": communities.data es una foto unica por
% comunidad (no trae meses). El modelo aprende la relacion
% variables -> nivel de crimen y se usa como pronostico: las variables medidas
% este mes dan el nivel esperado del mes siguiente. Si se dispone de datos
% mensuales, basta con armar X con las variables del mes t e y con el nivel
% del mes t+1 y el resto del codigo no cambia.

clc; clear; close all;

%% ------------------------- Configuracion -------------------------
cfg.archivo      = 'communities.data';
cfg.umbralCrimen = [];      % [] = mediana; o un valor fijo, p. ej. 0.20
cfg.fracEnt      = 0.70;    % entrenamiento
cfg.fracVal      = 0.20;    % validacion (el resto, 10%, es prueba)
cfg.pruebaFija   = true;    % true : el 10% de prueba se aparta una sola vez
                            %        (al azar) y ningun entrenamiento lo ve,
                            %        asi la exactitud final es honesta.
                            % false: el 10% de prueba tambien se re-permuta
                            %        en cada entrenamiento.

cfg.nOcultas     = 5;       % neuronas ocultas de la red
cfg.nBits        = 16;      % bits por peso
cfg.rango        = 8;       % pesos en [-rango, rango]

cfg.Ngen         = 150;     % generaciones maximas por entrenamiento
cfg.npop         = 80;      % tamano de la poblacion
cfg.nElite       = 2;       % individuos que pasan intactos
cfg.press        = 0.01;    % presion selectiva
cfg.pcross       = 0.8;     % probabilidad de cruce
cfg.pmut         = 0.004;   % probabilidad de mutacion por bit
cfg.pacienciaGen = 40;      % generaciones sin mejorar en validacion

cfg.maxRondas      = 30;    % rondas maximas de entrenamientos paralelos
cfg.pacienciaRonda = 6;     % rondas sin mejorar al campeon
cfg.mejoraMin      = 1e-3;  % mejora minima de costo que reinicia la paciencia
cfg.metaExacBal    = 0.90;  % meta de exactitud balanceada (seleccion)

%% ------------------------- Datos -------------------------
[X, y, crimen, umbral] = cargarDatosCrimen(cfg.archivo, cfg.umbralCrimen);
N = size(X, 1);
fprintf('Comunidades: %d | umbral de crimen: %.3f | ALTA: %d  BAJA: %d\n', ...
        N, umbral, sum(y == 1), sum(y == 0));

rng('shuffle');                                  % cada ejecucion es distinta
if cfg.pruebaFija
    perm      = randperm(N);
    idxPrueba = perm(1:(N - round(cfg.fracEnt*N) - round(cfg.fracVal*N)));
    idxSelec  = setdiff(1:N, idxPrueba);         % datos para elegir campeon
else
    idxPrueba = [];
    idxSelec  = [];
end

%% ------------------------- Paralelo -------------------------
nTareas = iniciarParalelo();                     % una tarea por nucleo

%% ------------------------- Rondas -------------------------
campeon      = [];
costoCampeon = inf;
cromCampeon  = [];
histRondas   = nan(cfg.maxRondas, 2);            % [costo exacBal] del campeon
sinMejora    = 0;
tInicio      = tic;

for ronda = 1:cfg.maxRondas
    semillas = randi(2^31 - 1, nTareas, 1);      % inicios aleatorios
    resul    = cell(nTareas, 1);

    parfor t = 1:nTareas
        resul{t} = entrenarGA(X, y, idxPrueba, cfg, semillas(t), cromCampeon);
    end

    % Puntaje comun para comparar a los candidatos de la ronda
    costoAntes = costoCampeon;
    for t = 1:nTareas
        r = resul{t};
        if cfg.pruebaFija
            [r.costoSelec, r.exacBalSelec] = ...
                costoGA(r.w, X(idxSelec, :), y(idxSelec), cfg.nOcultas);
        else
            r.costoSelec   = r.costoVal;
            r.exacBalSelec = r.exacBalVal;
        end
        if r.costoSelec < costoCampeon - 1e-9
            campeon      = r;
            costoCampeon = r.costoSelec;
            cromCampeon  = r.cromosoma;
        end
    end
    mejoro = costoCampeon < costoAntes - cfg.mejoraMin;

    if mejoro
        sinMejora = 0;              estado = 'mejora';
    else
        sinMejora = sinMejora + 1;  estado = 'sin mejora';
    end
    histRondas(ronda, :) = [costoCampeon campeon.exacBalSelec];
    fprintf(['Ronda %2d | campeon: costo %.4f | exac. bal. ent %.3f  ' ...
             'val %.3f  seleccion %.3f | %s\n'], ronda, costoCampeon, ...
             campeon.exacBalEnt, campeon.exacBalVal, campeon.exacBalSelec, ...
             estado);

    if campeon.exacBalSelec >= cfg.metaExacBal
        fprintf('Meta de exactitud alcanzada.\n');  break;
    end
    if sinMejora >= cfg.pacienciaRonda
        fprintf('Sin mejora en %d rondas: se detiene.\n', sinMejora);  break;
    end
end
histRondas = histRondas(1:ronda, :);
fprintf('Tiempo total: %.1f s\n', toc(tInicio));

%% ------------------------- Prueba final (10%) -------------------------
iP = campeon.iPrueba;
[~, exacBalP, exacP, conf] = costoGA(campeon.w, X(iP, :), y(iP), cfg.nOcultas);
fprintf('\n===== MEJOR MODELO: prueba con %d comunidades =====\n', numel(iP));
fprintf('Exactitud: %.2f %%   Exactitud balanceada: %.2f %%\n', ...
        100 * exacP, 100 * exacBalP);
fprintf('Matriz de confusion (filas = real, columnas = prediccion)\n');
fprintf('              pred BAJA   pred ALTA\n');
fprintf('  real BAJA   %8d   %8d\n', conf(1, 1), conf(1, 2));
fprintf('  real ALTA   %8d   %8d\n', conf(2, 1), conf(2, 2));

%% ------------------------- Guardar modelo -------------------------
modelo.w            = campeon.w;
modelo.cromosoma    = campeon.cromosoma;
modelo.nOcultas     = cfg.nOcultas;
modelo.umbralCrimen = umbral;
modelo.variables    = {'PctDivorcio', 'PctEmpleo', 'PctSinSecundaria', 'PctPobreza'};
modelo.exacPrueba   = exacP;
modelo.cfg          = cfg;
save('mejorModeloCrimen.mat', 'modelo', 'campeon', 'histRondas');
fprintf('\nModelo guardado en mejorModeloCrimen.mat\n');

%% ------------------------- Ejemplo de pronostico -------------------------
ejemplo = [0.75 0.40 0.55 0.60;     % mucho divorcio, poco empleo, mucha pobreza
           0.25 0.70 0.20 0.10];    % caso contrario
[nivel, prob] = predecirCrimen(modelo, ejemplo);
for i = 1:size(ejemplo, 1)
    fprintf('Medicion [%s] -> criminalidad %s el proximo mes (p = %.2f)\n', ...
            num2str(ejemplo(i, :), '%.2f '), nivel{i}, prob(i));
end

%% ------------------------- Graficas -------------------------
figure;
subplot(1, 2, 1);
plot(campeon.hist, 'linewidth', 1.5); grid on;
xlabel('Generacion'); ylabel('Costo');
legend('Mejor (entrenamiento)', 'Promedio (entrenamiento)', 'Mejor (validacion)');
title('Entrenamiento del campeon');
subplot(1, 2, 2);
plot(100 * histRondas(:, 2), '-o', 'linewidth', 1.5); grid on;
xlabel('Ronda'); ylabel('Exactitud balanceada (%)');
title('Campeon por ronda');
