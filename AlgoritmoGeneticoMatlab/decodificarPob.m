function W = decodificarPob(pop, nBits, rango)
% DECODIFICARPOB Convierte cromosomas binarios en pesos reales.
%   pop : nInd x (nPar*nBits) matriz de 0/1
%   W   : nInd x nPar, cada parametro en [-rango, rango]
nPar  = size(pop, 2) / nBits;
pesos = 2 .^ (nBits-1:-1:0)';
W = zeros(size(pop, 1), nPar);
for k = 1:nPar
    W(:, k) = pop(:, (k-1)*nBits + (1:nBits)) * pesos;
end
W = rango * (2 * W / (2^nBits - 1) - 1);
end
