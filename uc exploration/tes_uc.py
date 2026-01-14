from uc_explore import closure_of_antichain, compress_Cij

def test_closure():
    ant = [1<<0, 1<<1]  # {0}, {1}
    F = closure_of_antichain(ant)
    assert 0 in F
    assert (1<<0) in F and (1<<1) in F and ((1<<0)|(1<<1)) in F

def test_compress():
    F = { (1<<1), (1<<0)|(1<<1) }  # {1}, {0,1}
    F2 = compress_Cij(F, 0, 1)
    # {1} becomes {0}, {0,1} unchanged
    assert (1<<0) in F2
    assert ((1<<0)|(1<<1)) in F2
    print("compress_Cij tests ok")

if __name__ == "__main__":
    test_closure()
    test_compress()
