import numpy as np


def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
  examples, where each example x[i] has shape (d_1, ..., d_k). We will
  reshape each input into a vector of dimension D = d_1 * ... * d_k, and
  then transform it to an output vector of dimension M.

  Inputs:
  - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
  - w: A numpy array of weights, of shape (D, M)
  - b: A numpy array of biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """
  out = None
  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  # Reshape the matrix, letting numpy figure out what is the size of the newly
  # aggregated dimension D by passing it -1
  X = np.reshape(x,(x.shape[0],-1))
  # Just apply weight using matrix multiplication, then broadcast bias on each
  # line
  out = np.dot(X, w) + b
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  # out = X.W + b, hence dX = dout.w, dw = X.dout, db = dout * 1(N)
  dX = np.dot(dout,w.T)
  # Reshape dX to obtain dx
  dx = dX.reshape(x.shape)
  # Conversely, we need to reshape x to obtain dW
  dw = np.dot(x.reshape(dX.shape).T, dout)
  # This one is easy
  db = np.dot(dout.T,np.ones(x.shape[0]))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  # Take advantage of broadcasting to calculate out at once
  out = np.maximum(0,x)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  # A bit convoluted, but takes fill advantage of numpy
  dx = np.where( x >= 0, dout, 0)
  # ie dx is equal to dout whenever x is positive
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def batchnorm_forward(x, gamma, beta, bn_param):
  """
  Forward pass for batch normalization.
  
  During training the sample mean and (uncorrected) sample variance are
  computed from minibatch statistics and used to normalize the incoming data.
  During training we also keep an exponentially decaying running mean of the mean
  and variance of each feature, and these averages are used to normalize data
  at test-time.

  At each timestep we update the running averages for mean and variance using
  an exponential decay based on the momentum parameter:

  running_mean = momentum * running_mean + (1 - momentum) * sample_mean
  running_var = momentum * running_var + (1 - momentum) * sample_var

  Note that the batch normalization paper suggests a different test-time
  behavior: they compute sample mean and variance for each feature using a
  large number of training images rather than using a running average. For
  this implementation we have chosen to use running averages instead since
  they do not require an additional estimation step; the torch7 implementation
  of batch normalization also uses running averages.

  Input:
  - x: Data of shape (N, D)
  - gamma: Scale parameter of shape (D,)
  - beta: Shift paremeter of shape (D,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features

  Returns a tuple of:
  - out: of shape (N, D)
  - cache: A tuple of values needed in the backward pass
  """
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, D = x.shape
  running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
  running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

  out, cache = None, None
  if mode == 'train':
    #############################################################################
    # TODO: Implement the training-time forward pass for batch normalization.   #
    # Use minibatch statistics to compute the mean and variance, use these      #
    # statistics to normalize the incoming data, and scale and shift the        #
    # normalized data using gamma and beta.                                     #
    #                                                                           #
    # You should store the output in the variable out. Any intermediates that   #
    # you need for the backward pass should be stored in the cache variable.    #
    #                                                                           #
    # You should also use your computed sample mean and variance together with  #
    # the momentum variable to update the running mean and running variance,    #
    # storing your result in the running_mean and running_var variables.        #
    #############################################################################
    # Evaluate sample mean
    sample_mean = np.mean(x, axis=0)
    # Evaluate sample variance (note: broadcast on - )
    sample_var = np.mean(np.square(x - sample_mean), axis=0)
    # Normalize the input (note: triple broadcast on - , +, then /)
    num = x - sample_mean
    den = np.sqrt(sample_var + eps)
    xn = num/den
    # And scale to produce the output (note: broadcast on +)
    out = xn * gamma + beta
    # Update running mean and variance
    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var
    # Set cache values
    cache = gamma, beta, eps, x, xn, sample_mean, sample_var, num, den
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  elif mode == 'test':
    #############################################################################
    # TODO: Implement the test-time forward pass for batch normalization. Use   #
    # the running mean and variance to normalize the incoming data, then scale  #
    # and shift the normalized data using gamma and beta. Store the result in   #
    # the out variable.                                                         #
    #############################################################################
    # Normalize the input (note: triple broadcast on - , +, then /)
    xn = (x - running_mean)/(np.sqrt(running_var + eps))
    # And scale to produce the output (note: broadcast on +)
    out = xn * gamma + beta
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  # Store the updated running means back into bn_param
  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var

  return out, cache


def batchnorm_backward(dout, cache):
  """
  Backward pass for batch normalization.
  
  For this implementation, you should write out a computation graph for
  batch normalization on paper and propagate gradients backward through
  intermediate nodes.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, D)
  - cache: Variable of intermediates from batchnorm_forward.
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs x, of shape (N, D)
  - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
  - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #############################################################################
  gamma, beta, eps, x, xn, smean, svar, num, den = cache
  # out = gamma*xn + beta
  dxn = dout * gamma # Note the broadcast on *
  # Gamma and beta are actually matrix obtained by the replication of the
  # vectors along the first axis, so for the vector derivative, we need to sum
  # the value of all lines
  dgamma = np.sum(dout * xn, axis=0) # broadcast forward means sum backward
  dbeta = np.sum(dout, axis=0) # broadcast forward means sum backward
  # We now need to propagate dxn
  invden = 1.0/den
  # Evaluate first numerator gradient from dxn
  dnum = dxn * invden # Note the broadcast here
  # Initialize dsmean and dx with dnum contribution
  dx = 1.0 * dnum
  dsmean = -1.0 * np.sum(dnum, axis=0) # broadcast forward means sum backward
  # Evaluate inverted denominator gradient from dxn
  dinvden = np.sum(dxn * num, axis=0) # broadcast forward means sum backward
  # And now the actual denominator gradient
  dden = (-1.0 / np.square(den)) * dinvden # no dimension change here
  # Propagate dden on d(svar+eps). Note that we can reuse den as d(sqrt) is
  # 0.5/sqrt
  dsvareps = (0.5 / den) * dden # no dimension change here
  # dsvar is actually dssvareps
  dsvar = dsvareps
  # We must now evaluate the dsvar contribution to dx and dsmean
  # broadcast forward means sum backward, and dividing by N is actually mean
  dsmean += 2.0 * dsvar * np.mean(x - smean, axis=0)
  # No dimension change for dx
  dx += 2.0 * dsvar * (x - smean)/x.shape[0]
  # Finally we can propagate dsmean contribution on dx, expanded on all rows
  dx += np.ones(x.shape) * dsmean/x.shape[0]

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
  """
  Alternative backward pass for batch normalization.
  
  For this implementation you should work out the derivatives for the batch
  normalizaton backward pass on paper and simplify as much as possible. You
  should be able to derive a simple expression for the backward pass.
  
  Note: This implementation should expect to receive the same cache variable
  as batchnorm_backward, but might not use all of the values in the cache.
  
  Inputs / outputs: Same as batchnorm_backward
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #                                                                           #
  # After computing the gradient with respect to the centered inputs, you     #
  # should be able to compute gradients with respect to the inputs in a       #
  # single statement; our implementation fits on a single 80-character line.  #
  #############################################################################
  gamma, beta, eps, x, xn, smean, svar, num, den = cache
  N = x.shape[0]
  dx = N * dout - np.sum(dout, axis=0)
  dx -= (x - smean) * np.sum(dout * (x - smean),axis=0)/(svar + eps)
  dx *= gamma / N / np.sqrt(svar + eps)
  dgamma = np.sum(dout * xn, axis=0) # broadcast forward means sum backward
  dbeta = np.sum(dout, axis=0) # broadcast forward means sum backward
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
  """
  Performs the forward pass for (inverted) dropout.

  Inputs:
  - x: Input data, of any shape
  - dropout_param: A dictionary with the following keys:
    - p: Dropout parameter. We drop each neuron output with probability p.
    - mode: 'test' or 'train'. If the mode is train, then perform dropout;
      if the mode is test, then just return the input.
    - seed: Seed for the random number generator. Passing seed makes this
      function deterministic, which is needed for gradient checking but not in
      real networks.

  Outputs:
  - out: Array of the same shape as x.
  - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
    mask that was used to multiply the input; in test mode, mask is None.
  """
  p, mode = dropout_param['p'], dropout_param['mode']
  if 'seed' in dropout_param:
    np.random.seed(dropout_param['seed'])

  mask = None
  out = None

  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase forward pass for inverted dropout.   #
    # Store the dropout mask in the mask variable.                            #
    ###########################################################################
    mask = np.ones(x.shape)
    probs = np.random.rand(*x.shape) # Note we have to unpack the shape
    mask[ probs < p ] = 0
    out = x * mask
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    ###########################################################################
    # TODO: Implement the test phase forward pass for inverted dropout.       #
    ###########################################################################
    out = x
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

  cache = (dropout_param, mask)
  out = out.astype(x.dtype, copy=False)

  return out, cache


def dropout_backward(dout, cache):
  """
  Perform the backward pass for (inverted) dropout.

  Inputs:
  - dout: Upstream derivatives, of any shape
  - cache: (dropout_param, mask) from dropout_forward.
  """
  dropout_param, mask = cache
  mode = dropout_param['mode']
  
  dx = None
  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase backward pass for inverted dropout.  #
    ###########################################################################
    dx = dout * mask
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    dx = dout
  return dx


def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  
  # Convenience variables to hold dimension values
  N, C, H, W = x.shape
  F, C, HH, WW = w.shape
  # Special dimension used for reshaped matrices multiplication
  D = C*HH*WW
  # Extract stride and pad
  stride = conv_param.get("stride",1)
  pad = conv_param.get("pad",0)

  # First, add zero padding along height and width axis
  padding = ( (0,), (0,), (pad,), (pad,) )
  x_padded = np.pad(x,padding,'constant')
  
  # Evaluate number of operations along the height axis
  H1 = int(1 + (H + 2 * pad - HH) / stride)
  # Evaluate number of operations along the width axis
  W1 = int(1 + (W + 2 * pad - WW) / stride)
  # Create out matrix
  out = np.zeros((N, F, H1, W1))
  
  # We need a (D, F) reshaped filter matrix to perform matrix multiplication
  wr = w.reshape(F, D).T
  
  # Iterate along height and width to apply kernels
  for i in range(H1):
      for j in range(W1):
          # Isolate the subset of the image we apply the kernel on
          xij = x_padded[:,:, stride*i:stride*i + HH , stride*j:stride*j + WW]
          # Reshape the subset to use matrix multiplication
          xij = xij.reshape(N, D)
          # Multiply by reshaped filter and add bias to calculate output
          out[:,:,i,j] = np.dot(xij,wr) + b

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b, conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  #############################################################################
  # Retrieve cache
  x, w, b, conv_param = cache
  # Convenience dimension variables
  N, C, H, W = x.shape
  F, C, HH, WW = w.shape
  # Special dimension used for reshaped matrices multiplication
  D = C*HH*WW
  # Extract stride and pad
  stride = conv_param.get("stride",1)
  pad = conv_param.get("pad",0)

  # First, add zero padding along height and width axis
  padding = ( (0,), (0,), (pad,), (pad,) )
  x_padded = np.pad(x,padding,'constant')
  
  # Evaluate number of operations along the height axis
  H1 = int(1 + (H + 2 * pad - HH) / stride)
  # Evaluate number of operations along the width axis
  W1 = int(1 + (W + 2 * pad - WW) / stride)
  
  # We need a (D, F) reshaped filter matrix to perform matrix multiplication
  wr = w.reshape(F, D)

  # Initialize gradients
  # Note that we will get dw from the reshaped dwr
  dx_padded = np.zeros(x_padded.shape)
  dwr = np.zeros(wr.shape)
  db = np.zeros(b.shape)
  
  # Iterate along height and width to evaluate gradients
  for i in range(H1):
      for j in range(W1):
          # Isolate the subset of the output gradient that corresponds to this
          # kernel operation
          dO = dout[:,:,i,j]

          # It contributes to the gradient of only the subset of the input image
          # we applied the kernel on
          xij = x_padded[:,:, stride*i:stride*i + HH , stride*j:stride*j + WW]
          # Reshape the subset to use matrix multiplication
          xij = xij.reshape(N, D)

          # Calculate output gradient contributions to dxij, dwr, db

          # dxij = dout x wr
          dxij = np.dot(dO,wr)
          # Reshape to recover initial dimensions
          dxij = dxij.reshape(N, C, HH, WW)
          # Now apply this contribution to dx subset
          dx_padded[:,:, stride*i:stride*i+HH, stride*j:stride*j+WW] += dxij
          
          # dwr += dout.T x xij
          dwr += np.dot(dO.T,xij)
          
          # db += dout.T x 1(N) 
          db += np.dot(dO.T,np.ones(N))
  
  # Remove padding to obtain dx
  dx = dx_padded[:,:,pad:H+pad,pad:W+pad]
  
  # Reshape dwr to obtain dw
  dw = dwr.reshape(F, C, HH, WW)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  N, C, H, W = x.shape
  HH = pool_param.get("pool_height", H)
  WW = pool_param.get("pool_width", W)
  stride = pool_param.get("stride", 1)
  # Calculate output sizes
  H1 = int((H - HH)/stride + 1)
  W1 = int((W - WW)/stride + 1)
  # Initialize output
  out = np.zeros((N, C, H1, W1))
  # Iterate to populate output
  for i in range(H1):
      for j in range(W1):
          # Isolate the subset of input we work on
          xij = x[:,:, stride*i:stride*i+HH, stride*j:stride*j+WW]
          # Take the max value of the subset along the last two axis
          out[:,:,i,j] = np.amax(xij, axis=(2,3))

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, out, pool_param)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  dx = None
  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  x, out, pool_param = cache
  N, C, H, W = x.shape
  HH = pool_param.get("pool_height", H)
  WW = pool_param.get("pool_width", W)
  stride = pool_param.get("stride", 1)
  # Calculate output sizes
  H1 = int((H - HH)/stride + 1)
  W1 = int((W - WW)/stride + 1)
  # Initialize output
  dx = np.zeros((N, C, H, W))
  # Iterate to populate output
  for i in range(H1):
      for j in range(W1):
          # Isolate the subset of input we work on
          xij = x[:,:, stride*i:stride*i+HH, stride*j:stride*j+WW]
          # Also create convenience variables based on out/dout
          outij = out[:,:,i,j]
          doutij = dout[:,:,i,j]
          # Expand them to match xij size and ease numpy operations
          outij = np.repeat(outij, HH*WW).reshape(xij.shape)
          doutij = np.repeat(doutij, HH*WW).reshape(xij.shape)
          # Create a mask corresponding to max values
          maskij = xij == outij
          # Evaluate max function gradient (1.0 if max, 0.0 otherwise)
          dxij = np.zeros(xij.shape)
          dxij[ maskij ] = 1.0
          # Multiply by upstream gradient
          dxij *= doutij
          # Final step: apply to global gradient
          dx[:,:, stride*i:stride*i+HH, stride*j:stride*j+WW] += dxij
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """
  out, cache = None, None

  #############################################################################
  # TODO: Implement the forward pass for spatial batch normalization.         #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  N, C, H, W = x.shape
  # Put C dimension at the end then reshape the input
  rx = x.transpose(0, 2, 3, 1).reshape(N*H*W, C)
  # Apply vanilla batch normalization
  rout, cache = batchnorm_forward(rx, gamma, beta, bn_param)
  # Reshape the output and restore initial order of dimensions
  out = rout.reshape(N, H, W, C).transpose(0, 3, 1, 2)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return out, cache


def spatial_batchnorm_backward(dout, cache):
  """
  Computes the backward pass for spatial batch normalization.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, C, H, W)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs, of shape (N, C, H, W)
  - dgamma: Gradient with respect to scale parameter, of shape (C,)
  - dbeta: Gradient with respect to shift parameter, of shape (C,)
  """
  dx, dgamma, dbeta = None, None, None

  #############################################################################
  # TODO: Implement the backward pass for spatial batch normalization.        #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  N, C, H, W = dout.shape
  # Put C dimension at the end then reshape the input gradient
  rdout = dout.transpose(0, 2, 3, 1).reshape(N*H*W, C)
  # Apply vanilla batch normalization
  rdx, dgamma, dbeta = batchnorm_backward_alt(rdout, cache)
  # Reshape the output gradient and restore initial order of dimensions
  dx = rdx.reshape(N, H, W, C).transpose(0, 3, 1, 2)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta
  

def svm_loss(x, y):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  N = x.shape[0]
  correct_class_scores = x[np.arange(N), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(N), y] = 0
  loss = np.sum(margins) / N
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(N), y] -= num_pos
  dx /= N
  return loss, dx


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  N = x.shape[0]
  loss = -np.sum(np.log(probs[np.arange(N), y])) / N
  dx = probs.copy()
  dx[np.arange(N), y] -= 1
  dx /= N
  return loss, dx
