function [X, y, crimen, umbral] = cargarDatosCrimen(archivo, umbral)
% CARGARDATOSCRIMEN Lee communities.data (UCI "Communities and Crime").
%   X      : N x 4  [PctDivorcio PctEmpleo PctSinSecundaria PctPobreza] (0..1)
%   y      : N x 1  1 = criminalidad ALTA, 0 = criminalidad BAJA
%   crimen : N x 1  indice de crimen violento por habitante (0..1)
%   umbral : valor de corte usado (si llega vacio se usa la mediana, lo que
%            deja las dos clases balanceadas)

% Columnas del archivo original (128 atributos):
%   47 TotalPctDiv, 39 PctEmploy, 36 PctNotHSGrad, 34 PctPopUnderPov,
%   128 ViolentCrimesPerPop
cols = [47 39 36 34 128];

texto  = fileread(archivo);
lineas = regexp(texto, '\r?\n', 'split');
lineas = lineas(~cellfun(@isempty, lineas));

datos = nan(numel(lineas), numel(cols));
for i = 1:numel(lineas)
    campos = regexp(lineas{i}, ',', 'split');
    if numel(campos) >= max(cols)
        datos(i, :) = str2double(campos(cols));   % '?' -> NaN
    end
end
datos = datos(~any(isnan(datos), 2), :);          % descarta filas incompletas

X      = datos(:, 1:4);
crimen = datos(:, 5);
if nargin < 2 || isempty(umbral)
    umbral = median(crimen);
end
y = double(crimen > umbral);
end
