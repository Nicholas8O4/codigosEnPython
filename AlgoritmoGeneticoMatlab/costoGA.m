function [costo, exacBal, exac, conf] = costoGA(w, X, y, nOcultas)
% COSTOGA Funcion objetivo (a minimizar) de un individuo.
%   costo   = (1 - exactitud balanceada) + 0.25 * entropia cruzada
%   exacBal = promedio de sensibilidad y especificidad
%   exac    = exactitud global
%   conf    = matriz de confusion [VN FP; FN VP] (filas = real, cols = prediccion)
p    = redCrimen(w, X, nOcultas);
p    = min(max(p, 1e-12), 1 - 1e-12);
pred = p >= 0.5;

VP = sum(pred & y == 1);   FN = sum(~pred & y == 1);
VN = sum(~pred & y == 0);  FP = sum(pred & y == 0);

sens    = VP / max(VP + FN, 1);
espec   = VN / max(VN + FP, 1);
exacBal = (sens + espec) / 2;
exac    = (VP + VN) / numel(y);
bce     = -mean(y .* log(p) + (1 - y) .* log(1 - p));

costo = (1 - exacBal) + 0.25 * bce;
conf  = [VN FP; FN VP];
end
