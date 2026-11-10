function [nivel, prob] = predecirCrimen(modelo, X)
% PREDECIRCRIMEN Nivel de criminalidad esperado para el proximo mes.
%   modelo : estructura guardada en mejorModeloCrimen.mat
%   X      : M x 4 con las mediciones del mes actual, en la misma escala
%            0..1 del dataset:
%            [PctDivorcio PctEmpleo PctSinSecundaria PctPobreza]
%   nivel  : M x 1 celda con 'ALTA' o 'BAJA'
%   prob   : M x 1 probabilidad de criminalidad ALTA
%
% Ejemplo:
%   load mejorModeloCrimen.mat modelo
%   [nivel, prob] = predecirCrimen(modelo, [0.75 0.40 0.55 0.60])
prob  = redCrimen(modelo.w, X, modelo.nOcultas);
nivel = repmat({'BAJA'}, size(X, 1), 1);
nivel(prob >= 0.5) = {'ALTA'};
end
