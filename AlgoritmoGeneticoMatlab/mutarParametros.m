function cfg = mutarParametros(cfg)
% MUTARPARAMETROS Sortea nuevos parametros del algoritmo genetico.
%   Se usa cuando el entrenamiento se estanca. Solo cambia parametros de la
%   busqueda (no la estructura de la red ni la codificacion), de modo que el
%   cromosoma del campeon sigue siendo valido y se puede seguir desde el.
tamanos    = [60 80 120 160];
cfg.npop   = tamanos(randi(numel(tamanos)));          % tamano de poblacion
cfg.pmut   = 10 ^ (-3 + 1.3 * rand);                  % 0.001 .. 0.02
cfg.pcross = 0.6 + 0.35 * rand;                       % 0.60 .. 0.95
cfg.press  = 10 ^ (-2.3 + 1.3 * rand);                % 0.005 .. 0.1
cfg.nElite = randi(4);                                % 1 .. 4
end
