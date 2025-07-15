def smarts_attack_dlog(P, Q, l):
    C = P.curve()
    R = R
    assert C == Q.curve()
    assert R.is_finite()
    
    pe = R.characteristic()
    p, e = is_prime_power(pe, get_data=True)
    assert e > 0
    E_Qp = EllipticCurve(Qp(p, prec=l+5, print_mode='series'), [ZZ(t) + randrange(p)*p**l for t in C.a_invariants()])
    if l == 1:
        for P_cand in E_Qp.lift_x(ZZ(P.x()), all=True):
            if R(P_cand.y()) == P.y():
                break
        else:
            raise ValueError
        P_Qp = P_cand
        for Q_cand in E_Qp.lift_x(ZZ(Q.x()), all=True):
            if R(Q_cand.y()) == Q.y():
                break
        else:
            raise ValueError
        Q_Qp = Q_cand
    else:
        P_Qp = E_Qp(P)
        Q_Qp = E_Qp(Q)

    E_p = EllipticCurve(Zmod(p), C.a_invariants())
    order_p = E_p.order()

    P_ = order_p * P_Qp
    Q_ = order_p * Q_Qp
    
    zP = -P_[0] / P_[1]
    zQ = -Q_[0] / Q_[1]
    
    k0 = Mod(zQ / zP, p)
    known_k = Integer(k0)
    
    for i in range(1, l-1):
        Q_i = Q_Qp - known_k * P_Qp
        
        P_i = (p**i) * P_Qp
        
        Q_i_ = order_p * Q_i
        P_i_ = order_p * P_i

        z_Qi = -Q_i_[0] / Q_i_[1]
        z_Pi = -P_i_[0] / P_i_[1]
        
        ki = Mod(z_Qi / z_Pi, p)
        
        known_k += Integer(ki) * (p**i)
        
    return known_k
