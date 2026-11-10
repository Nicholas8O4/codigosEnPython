function res = entrenarGA(X, y, idxPruebaFija, cfg, semilla, mejorPrevio)
% ENTRENARGA Un entrenamiento genetico completo (una "tarea" paralela).
%   - Permuta los datos al azar y los divide 70% / 20% / 10%.
%   - Poblacion inicial aleatoria; si llega mejorPrevio (cromosoma del ultimo
%     mejor individuo) se inyecta para conservar sus caracteristicas.
%   - Evoluciona con ruleta + cruce uniforme + mutacion + elitismo.
%   - Devuelve el individuo con mejor desempeno en VALIDACION.

rng(semilla, 'twister');                 % inicio aleatorio distinto por tarea

%% ---- Permutacion aleatoria y division 70 / 20 / 10 ----
N    = size(X, 1);
nEnt = round(cfg.fracEnt * N);
nVal = round(cfg.fracVal * N);
if isempty(idxPruebaFija)
    perm    = randperm(N);
    iEnt    = perm(1:nEnt);
    iVal    = perm(nEnt + (1:nVal));
    iPrueba = perm(nEnt + nVal + 1:end);
else
    resto   = setdiff(1:N, idxPruebaFija);
    resto   = resto(randperm(numel(resto)));
    iEnt    = resto(1:nEnt);
    iVal    = resto(nEnt + 1:end);
    iPrueba = idxPruebaFija(:)';
end
Xe = X(iEnt, :);  ye = y(iEnt);
Xv = X(iVal, :);  yv = y(iVal);

%% ---- Poblacion inicial aleatoria ----
nPar   = 4 * cfg.nOcultas + 2 * cfg.nOcultas + 1;
totpar = nPar * cfg.nBits;
pop    = double(rand(cfg.npop, totpar) < 0.5);
if ~isempty(mejorPrevio)
    pop(1, :) = mejorPrevio;             % conserva al ultimo mejor individuo
end

fobj       = zeros(cfg.npop, 1);
hist       = nan(cfg.Ngen, 3);           % [mejorEnt promedioEnt mejorVal]
mejorVal   = inf;
mejorCrom  = pop(1, :);
sinMejora  = 0;

for k = 1:cfg.Ngen
    %% Evaluacion de todos los individuos (entrenamiento)
    W = decodificarPob(pop, cfg.nBits, cfg.rango);
    for j = 1:cfg.npop
        fobj(j) = costoGA(W(j, :), Xe, ye, cfg.nOcultas);
    end
    [~, orden] = sort(fobj);

    %% Validacion de los mejores de la generacion
    sinMejora = sinMejora + 1;
    for j = orden(1:cfg.nElite)'
        cVal = costoGA(W(j, :), Xv, yv, cfg.nOcultas);
        if cVal < mejorVal - 1e-9
            mejorVal  = cVal;
            mejorCrom = pop(j, :);
            sinMejora = 0;
        end
    end
    hist(k, :) = [fobj(orden(1)) mean(fobj) mejorVal];
    if sinMejora >= cfg.pacienciaGen
        break;                           % parada temprana
    end

    %% Seleccion por ruleta con presion selectiva
    fMax = max(fobj);  fMin = min(fobj);
    efic  = (1 - cfg.press) * (fMax - fobj) / max(fMax - fMin, eps) + cfg.press;
    rueda = cumsum(efic);
    nHijos = cfg.npop - cfg.nElite;
    idx1 = zeros(nHijos, 1);  idx2 = zeros(nHijos, 1);
    for j = 1:nHijos
        idx1(j) = find(rueda >= rand * rueda(end), 1);
        idx2(j) = find(rueda >= rand * rueda(end), 1);
    end
    padre1 = pop(idx1, :);
    padre2 = pop(idx2, :);

    %% Cruce uniforme
    mascara = rand(nHijos, totpar) < 0.5;
    cruza   = rand(nHijos, 1) < cfg.pcross;
    mascara(~cruza, :) = true;           % sin cruce: copia del padre 1
    hijos = padre2;
    hijos(mascara) = padre1(mascara);

    %% Mutacion bit a bit
    muta = rand(nHijos, totpar) < cfg.pmut;
    hijos(muta) = 1 - hijos(muta);

    %% Nueva generacion con elitismo
    pop = [pop(orden(1:cfg.nElite), :); hijos];
end

%% ---- Resultado de la tarea ----
w = decodificarPob(mejorCrom, cfg.nBits, cfg.rango);
res.cromosoma = mejorCrom;
res.w         = w;
[res.costoEnt, res.exacBalEnt] = costoGA(w, Xe, ye, cfg.nOcultas);
[res.costoVal, res.exacBalVal] = costoGA(w, Xv, yv, cfg.nOcultas);
[res.costoPrueba, res.exacBalPrueba, res.exacPrueba, res.confPrueba] = ...
    costoGA(w, X(iPrueba, :), y(iPrueba), cfg.nOcultas);
res.iEnt = iEnt;  res.iVal = iVal;  res.iPrueba = iPrueba;
res.hist = hist(1:k, :);
res.generaciones = k;
end
