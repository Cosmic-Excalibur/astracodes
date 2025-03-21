def known_pq(p, q, c, e = 0x10001):
    return pow(c, pow(e, -1, (p-1)*(q-1)), p*q)

rsa_known_pq = known_pq

def known_p(p, n, c, e = 0x10001):
    assert n % p == 0
    return pow(c, pow(e, -1, (p-1)*(n//p-1)), n)

rsa_known_p = known_p
