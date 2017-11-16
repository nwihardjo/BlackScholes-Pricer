def shark(spot, strike, tau, rate, vola, steps):
    """Fake numerical model by using noise."""
    #ref = bs.bscall(spot, strike, tau, rate, vola)

    endReturns = lambda ul, dl, N, initial: [((ul**k)*(dl)**(N-k))*initial for k in range(0, N+1)]
    final = lambda pstar, arr, r, t: [np.exp(-r*t)*(arr[0+i]*(1-pstar)+arr[1+i]*pstar) for i in range(0, len(arr)-1)]

    deltaT = tau/steps
    u = np.exp(vola * np.sqrt(deltaT))
    d = 1/u
    p = (np.exp(rate * deltaT) - d)/(u-d)
    discountFactor = np.exp(rate * deltaT)

    finalValue = endReturns(u,d,steps,spot)
    pStar = (discountFactor-d)/(u-d)
    
    BackwardLast = np.array([max(finalValue[i]-strike, 0.) for i in range(0, steps+1)])
    for i in range(0, steps):
        BackwardLast = final(pStar, BackwardLast, rate, deltaT)

    return BackwardLast

pricer = partial(shark,)
