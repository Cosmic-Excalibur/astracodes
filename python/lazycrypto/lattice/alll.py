# https://github.com/shx-lyu/algebraic-lll/blob/master/ALLLboost.m

def ALLLBoostCDF(B, d=1, delta=0.99):
    base_ring = B.base_ring()
    m = B.nrows()
    n = B.ncols()
    # Convert to complex matrices for numerical stability
    B = B.change_ring(CDF).T
    Q, R = B.QR()
    i = 2  # MATLAB uses 1-based indexing, start from column 2
    R = copy(R)

    while i <= n:
        current_i = i - 1  # Convert to 0-based index
        Ri = R.column(current_i)  # Backup the original column

        # Size reduction
        for k in range(i-2, -1, -1):  # MATLAB k from i-1 downto 1
            mu = R[k, current_i] / R[k, k]
            q = _quan(mu, d)
            if q != 0:
                # Subtract q*R[:,k] from R[:,current_i]
                R.set_column(current_i, R.column(current_i) - q * R.column(k))

        # Check if we need to revert the reduction
        if R.column(current_i).norm() > Ri.norm():
            # Check if the quantization of the original element is zero
            original_mu = Ri[i-2] / R[i-2, i-2]
            if _quan(original_mu, d) == 0:
                R.set_column(current_i, Ri)

        # Lovász condition
        lovasz_lhs = delta * abs(R[i-2, i-2])**2
        lovasz_rhs = abs(R[i-1, i-1])**2 + abs(R[i-2, i-1])**2

        if lovasz_lhs > lovasz_rhs:
            # Swap columns i-1 and i (0-based indices current_i-1 and current_i)
            col_prev = R.column(current_i-1)
            col_curr = R.column(current_i)
            R.set_column(current_i-1, col_curr)
            R.set_column(current_i, col_prev)

            # Compute Givens rotation parameters
            a = R[i-2, current_i-1]
            b = R[i-1, current_i-1]
            tempsum = sqrt(abs(a)**2 + abs(b)**2)
            if tempsum == 0:
                alpha = CDF(1)
                beta = CDF(0)
            else:
                alpha = a / tempsum
                beta = b / tempsum

            # Construct Givens matrix
            G = matrix.identity(CDF, m)
            G[i-2, i-2] = alpha.conjugate()
            G[i-2, i-1] = beta.conjugate()
            G[i-1, i-2] = -beta
            G[i-1, i-1] = alpha

            # Apply Givens rotation
            R = G * R
            Q = Q * G.conjugate().transpose()

            # Decrement index
            i = max(i-1, 2)
        else:
            i += 1

    res = (Q * R).T
    if d == 1:
        return matrix(base_ring, [vector(base_ring([round(round(x)) for x in z]) for z in v) for v in res])
    else:
        return res    # not implemented yet :p

def _quan(x, d=1):
    if (-d) % 4 == 1:
        # Type II (Eisenstein-like)
        sqrt_d = sqrt(d)
        sqrt_neg_d = 1j * sqrt_d
        s = 0.5 + 0.5 * sqrt_neg_d

        # Calculate r1
        r1_real = round(x.real())
        r1_imag = round(x.imag() / sqrt_d)
        r1 = r1_real + sqrt_neg_d * r1_imag

        # Calculate r2
        x_shifted = x - s
        r2_real = round(x_shifted.real())
        r2_imag = round((x_shifted.imag() - 0.5*sqrt_d) / sqrt_d)
        r2 = r2_real + sqrt_neg_d * r2_imag + s

        # Choose closer one
        if abs(x - r1) < abs(x - r2):
            return r1
        else:
            return r2
    else:
        # Type I (Gaussian-like)
        sqrt_neg_d = 1j * sqrt(d)
        r_real = round(x.real())
        r_imag = round(x.imag() / sqrt(d))
        return r_real + sqrt_neg_d * r_imag
