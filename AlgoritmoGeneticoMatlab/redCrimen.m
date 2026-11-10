function p = redCrimen(w, X, nOcultas)
% REDCRIMEN Red neuronal 4 -> nOcultas (tanh) -> 1 (sigmoide).
%   w : vector de pesos (nEnt*nOcultas + nOcultas + nOcultas + 1)
%   X : N x nEnt con las variables en escala 0..1
%   p : N x 1 probabilidad de criminalidad ALTA
nEnt = size(X, 2);
w  = w(:);
i1 = nEnt * nOcultas;
W1 = reshape(w(1:i1), nOcultas, nEnt);
b1 = w(i1 + (1:nOcultas))';
W2 = w(i1 + nOcultas + (1:nOcultas));
b2 = w(end);

Xn = 2 * X - 1;                                   % 0..1 -> -1..1
H  = tanh(Xn * W1' + repmat(b1, size(X, 1), 1));
p  = 1 ./ (1 + exp(-(H * W2 + b2)));
end
