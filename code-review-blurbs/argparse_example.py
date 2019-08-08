from __future__ import print_function, division
import argparse as ap


def _check_zoom(s):
    msg = "{} is not a valid zoom option".format(s)
    if s == 'auto':
        return(s)
    elif 'x' in s:
        try:
            a = float(s.split('x')[0])
            b = float(s.split('x')[1])
        except ValueError:
            raise ap.ArgumentTypeError(msg)
    elif ',' in s:
        try:
            a = float(s.split(',')[0])
            b = float(s.split(',')[1])
        except ValueError:
            raise ap.ArgumentTypeError(msg)
    else:
        raise ap.ArgumentTypeError(msg)

    return(s)


def _lower_case(s):
    return(s.lower())


def proc_args():
    pars = ap.ArgumentParser(description="Make plots for SUPERB V")
    pars.add_argument("-p1", "--ppdot", action="store_true",
                      help="Make P-Pdot diagram; requires path to db_file")
    pars.add_argument("-d", "--db_file", help="Path to db_file")
    pars.add_argument("-p2", "--profiles", action="store_true",
                      help="Plot grid of all pulsar profiles")
    pars.add_argument("-p3", "--histos", action="store_true",
                      help="Plot grid of all pulsar flux histograms")
    pars.add_argument("-r", "--rrat", dest="rrat_file",
                      help="Plot waterfall and profile of J1646-1910 "
                      "from given data file")
    pars.add_argument("-S", "--plot_pol", action="store_true")
    pars.add_argument("-A", "--archive")
    pars.add_argument("-T", "--tscrunch", action="store_true")
    pars.add_argument("-F", "--fscrunch", action="store_true")
    pars.add_argument("-b", "--bscrunch", type=int,
                      help="Scrunch bins by this factor")
    pars.add_argument("-p", "--pscrunch", action="store_true",
                      help="Polarisation scrunch")
    pars.add_argument("-g", "--output", default="1/xs",
                      help="Output file for plotting (1/xs -> plt.show)")
    pars.add_argument("-C", "--centre", action="store_true")
    pars.add_argument("-z", "--zoom_phase", type=_check_zoom,
                      help="Zoom on phase (specified as XxY or X,Y or "
                      "'auto' to automatically zoom on main pulse; "
                      "implies -C).")
    pars.add_argument("-y", "--zoom_y", type=_check_zoom,
                      help="Zoom the y-axis")
    pars.add_argument("-w", "--waterfall", action="store_true")
    return(vars(pars.parse_args()))

