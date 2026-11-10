function nTrab = iniciarParalelo()
% INICIARPARALELO Abre un pool con TODOS los nucleos del procesador.
%   Devuelve el numero de trabajadores. Si no esta el Parallel Computing
%   Toolbox, el parfor del programa principal se ejecuta en serie.
try
    nNucleos = feature('numcores');
catch
    nNucleos = 4;
end
nTrab = nNucleos;
try
    p = gcp('nocreate');
    if isempty(p)
        c = parcluster();                         % perfil por defecto
        c.NumWorkers = max(c.NumWorkers, nNucleos);
        p = parpool(c, nNucleos);
    end
    nTrab = p.NumWorkers;
    fprintf('Pool paralelo activo con %d trabajadores.\n', nTrab);
catch err
    fprintf(['Sin pool paralelo (%s).\n' ...
             'Las %d tareas de cada ronda se ejecutaran en serie.\n'], ...
             err.message, nTrab);
end
end
