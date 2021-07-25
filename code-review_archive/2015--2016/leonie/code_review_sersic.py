
filename2='code_review_data.fits'

hdulist2=fits.open(filename2)



Subaru_comp = hdulist2[1].data
Gmag='Gmag'
Imag='Imag'
Rmag='Rmag'
Dist = 'GDist'
GDist=Subaru_comp['GDist']





def many_sersic_tests( ): # function to plot the result of several sersic tests

    plt.figure( 5 ) ; plt.clf()
    result_list = [ test_sersic_fitting( seed=None )
                    for i in xrange( 30 ) ]
    return np.array( result_list )

def test_sersic_fitting():#m=2.5, Re=300., Ntot=800, seed=3121 ): # input as firstguesses in pars 
#Ntot should be the total number of GCs originally contained in sample

    
    xdata = np.true_divide(GDist[(Subaru_comp[Imag]>=22.5)],60) #generate_fake_GC_data( m, Re, Ntot, seed=seed ) 

    def sersic_negloglike(pars,xdata, Rtrunc=12.5 ):
        [ m, Re ] = pars
        loglike = np.log( 2. * np.pi * xdata 
                          * sersic_profile( xdata, m=m, Re=Re, Rtrunc=Rtrunc ) )
        result = - np.nansum( loglike ) + np.log( m ) + np.log( Re )#+ np.log( bg )
        #print 'index:',m,'Re:', Re,'result:', result
        return result
        
    firstguess = ( 1.5, 3.5)
    result = opt.fmin( sersic_negloglike, firstguess, args=(xdata,) )

    R = np.arange( 1.e-3, 20.+1e-4, 1e-3 ) * Re
    #print R
    dLdR = sersic_profile( R, *result, Rtrunc=12.5 )# change truncation radius
    L = integrate.cumtrapz( 2. * np.pi * R * dLdR, R )
    L /= L.max()

    plt.figure( 2 )
    plt.plot( R[:-1] / result[1], xdata.size*L, 'b-', lw=2, zorder=-1 )
    ###### testing for the change of n for different radii
    mm = np.arange( 1., 10., 0.01 ) 
    thing = np.array( [ sersic_negloglike( [m, Re], xdata ) for m in mm ] )
    #print thing
    plt.figure( 1 )  ; plt.clf()
    plt.plot( mm, 10**(-(thing-thing.min())), 'k-' )
    #plt.ylim( -thing.min() - 30 , -thing.min() + 10 )
    #print thing
    
    
    
    dLdR0 = sersic_profile( R, m, Re, Rtrunc=12.5 )

    L0 = integrate.cumtrapz( 2. * np.pi * R * (dLdR0), R )

    plt.figure( 5 )
    plt.plot( R[:-1], L, 'b-', alpha=.1 ) #np.cumsum( 2. * np.pi * R * dLdR ), 'r-' )
    plt.plot( R[:-1], L0, 'r-', alpha=.1 ) #np.cumsum( 2. * np.pi * R * dLdR0 ), 'b-' )
    plt.plot( np.sort( xdata ), np.linspace( 0., 1., xdata.size ),
               'k-', drawstyle='steps-pre', alpha=.1 )

    #firstguess = ( 2., 250.,0.0001 )
    #result = opt.fmin( sersic_negloglike, firstguess, args=(xdata,) )

    #R = np.arange( 1.e-3, 20.+1e-4, 1e-3 ) * Re
    #print R
    #dLdR = sersic_profile( R, *result, Rtrunc=800. )# change truncation radius
    #L = integrate.cumtrapz( 2. * np.pi * R * dLdR, R )
    #L /= L.max()

    #plt.figure( 2 )
    #plt.plot( R[:-1] / result[1], xdata.size*L, 'b-', lw=2, zorder=-1 )

    #rr = np.arange( 100., 750., 1 ) 
    #thing_r = np.array( [ sersic_negloglike( [m, Re], xdata ) for Re in rr ] )
    #print thing
    #plt.figure( 6 )  ; plt.clf()
    #plt.plot( rr, 10**(-(thing_r-thing_r.min())), 'k-' )



    return result
    
# ______________________________________________________________________________
# ______________________________________________________________________________

def generate_fake_GC_data( m=1.5, Re=250., Ntot=800, seed=3121 ): # generates fake data 
#    print seed
    if seed > 0 :                    
        np.random.seed( seed )
    logRonRe = np.linspace( -2., 3., 5001 )
    R = Re * 10**logRonRe

    R = np.arange( 0.e-3, 20.+1e-4, 1e-3 ) * Re
    dLdR = sersic_profile( R, m, Re )

    L = integrate.cumtrapz( 2. * np.pi * R * dLdR, R ) # 2 pi in there for normalisation?
    L = np.hstack( [0., L] )
    L /= L.max()
    
    x = np.interp( np.random.rand( Ntot ), L, R )

    plt.figure( 2 ) ; plt.clf()
    plt.plot( R/Re, Ntot*L, 'r-' )
    plt.plot( np.sort( x )/Re, np.arange( x.size ), 
              'k-', drawstyle='steps-pre' )

    return x
    
# ______________________________________________________________________________
# ______________________________________________________________________________

def sersic_profile( R, m, Re=1., N=1., Rtrunc=12.5 ):
    # where R is the inout radii easures
    # mn is the sersic index
    # Re and N are the firt guesses for the effective radius and the surface density of
    # GCs at the effective radius (that why we have to have the normalisation factor as the total number is defined by the integral)
    #The truncation radius is important due to the slope having a massive influence on how many GCs will be found 
    #
    #
    b = sersic_b( m ) # defines bn where we used an approximation for bn beforehand! see Pota et al.
    norm = ( Re**2. * 2.*np.pi * m * np.exp( b )
             / ( b**( 2.*m ) ) * gamma( 2.*m ) )# define the normalisation factor which is needed because N != Ntot /2 
    if Rtrunc > 0 :
        x = b * (Rtrunc / Re)**(1./m)
        norm *= gammainc( 2.*m, x ) 
    f = ((N * np.exp( -b * ( (R / Re)**(1./m) - 1. ) )+0.5557) / norm )
    if Rtrunc > 0 : # truncation radius has a large influence on how many objects one ends up with (variation in slope etc.). make sure to define a truncation radius where possible
        return np.where( R <= Rtrunc, f, np.nan )
    else :
        return f 
# ______________________________________________________________________________

def sersic_b( m ):
    return opt.brentq( sersic_to_solve, 0., 2. * m, args=(m,),
                       xtol=1e-6, rtol=1e-6 )
# ______________________________________________________________________________

def sersic_to_solve( bm, m ):
    # solution to eq 4 in Graham & Driver (2005)
    # note different definition of gammainc compared to G&D05!!!
    return gamma( 2*m ) * ( 1 - 2. * gammainc(2*m, bm) )
# ______________________________________________________________________________
# ______________________________________________________________________________