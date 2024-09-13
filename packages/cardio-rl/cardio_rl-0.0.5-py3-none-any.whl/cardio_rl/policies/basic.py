import torch as th
import numpy as np

class BasePolicy():
    def __init__(self, env, recurrent=False, hidden_dims=0):
        self.env = env        
        self.recurrent = recurrent
        self.hidden_dims = hidden_dims
        self.hidden = th.zeros(1, hidden_dims)
        
    def __call__(self, state, net):
        return self.env.action_space.sample()
    
    def reset(self):
        self.hidden = th.zeros(1, self.hidden_dims)
        # for policies that require resets, like NoisyNet or OuNoise
        # raise NotImplementedError
 
class WhitenoiseDeterministic(BasePolicy):
    def __init__(self, env):
        super().__init__(env)
        
    def __call__(self, state, net):
        input = th.from_numpy(state).float()  
        out = net(input)         
        mean = th.zeros_like(out)
        noise = th.normal(mean=mean, std=0.1)   # .clamp(-0.5, 0.5) # unsure if necessary... need to check other implementations
        out = (out + noise)    
        return out.clamp(-1, 1).detach().numpy()
                 

class EpsilonArgmax(BasePolicy):
    def __init__(self, env, eps=0.0, min_eps=0.0, ann_coeff=0.9, recurrent=False, hidden_dims=0):
        super().__init__(env, recurrent, hidden_dims)
        self.eps = eps
        self.min_eps = min_eps
        self.ann_coeff = ann_coeff

    def __call__(self, state, net):
        input = th.from_numpy(state).float()

        if np.random.rand() > self.eps:
            self.eps = max(self.min_eps, self.eps*self.ann_coeff)   
            if self.recurrent:
                out, self.hidden = net(input, hidden=self.hidden)
                out = out.detach().numpy()
            else: 
                out = net(input).detach().numpy()

            return np.argmax(out)  

        else:
            self.eps = max(self.min_eps, self.eps*self.ann_coeff)
            return self.env.action_space.sample()


class Gaussian(BasePolicy):
    def __init__(self, env):
        super().__init__(env)

    def __call__(self, state, net):
        input = th.from_numpy(state).float()
        mean, log_std = net(input)
        std = log_std.exp()

        dist = th.distributions.Normal(mean, std)
        a_sampled = th.nn.Tanh()(dist.rsample()).detach()

        return a_sampled.numpy() * self.env.action_space.high + 0


class NoisyNaf(BasePolicy):
    def __init__(self, env):
        super().__init__(env)

    def __call__(self, state, net):
        input = th.from_numpy(state).float()
        out, _, _, _ = net(input)
        return out.detach().numpy()


class Categorical(BasePolicy):
    def __init__(self, env):
        super().__init__(env)

    def __call__(self, state, net):
        input = th.from_numpy(state).float()
        probs = net(input)
        dist = th.distributions.Categorical(probs)
        return dist.sample().detach().numpy()
    
class Beta(BasePolicy):
    def __init__(self, env):
        super().__init__(env)

    def __call__(self, state, net):
        input = th.from_numpy(state).float()
        alpha, beta = net(input)
        dist = th.distributions.Beta(alpha, beta)
        return dist.sample().detach().numpy()