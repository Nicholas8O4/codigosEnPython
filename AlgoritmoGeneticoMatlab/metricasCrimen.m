function m = metricasCrimen(p, y)
% METRICASCRIMEN Curva ROC e indices de desempeno de un clasificador binario.
%   p : N x 1 probabilidad de clase ALTA      y : N x 1 clase real (0/1)
%   m.auc                 area bajo la curva ROC
%   m.fpr, m.tpr          puntos de la curva ROC (1-especificidad, sensibilidad)
%   m.exac, m.exacBal     exactitud y exactitud balanceada (corte 0.5)
%   m.sens, m.espec       sensibilidad (recall) y especificidad
%   m.precision, m.f1     precision y puntaje F1
%   m.mcc                 coeficiente de correlacion de Matthews
%   m.conf                matriz de confusion [VN FP; FN VP]
p = p(:);  y = y(:);

%% Curva ROC: se recorre el corte de mayor a menor probabilidad
[ps, orden] = sort(p, 'descend');
ys   = y(orden);
vp   = cumsum(ys == 1);
fp   = cumsum(ys == 0);
fin  = [diff(ps) ~= 0; true];            % ultimo elemento de cada empate
m.tpr = [0; vp(fin) / max(sum(y == 1), 1)];
m.fpr = [0; fp(fin) / max(sum(y == 0), 1)];
m.auc = trapz(m.fpr, m.tpr);

%% Indices con corte 0.5
pred = p >= 0.5;
VP = sum(pred & y == 1);   FN = sum(~pred & y == 1);
VN = sum(~pred & y == 0);  FP = sum(pred & y == 0);

m.sens      = VP / max(VP + FN, 1);
m.espec     = VN / max(VN + FP, 1);
m.precision = VP / max(VP + FP, 1);
m.exac      = (VP + VN) / numel(y);
m.exacBal   = (m.sens + m.espec) / 2;
m.f1        = 2 * m.precision * m.sens / max(m.precision + m.sens, eps);
m.mcc       = (VP * VN - FP * FN) / ...
              max(sqrt((VP + FP) * (VP + FN) * (VN + FP) * (VN + FN)), eps);
m.conf      = [VN FP; FN VP];
end
