import pyhepmc
import os
import argparse
import hist
import matplotlib.pyplot as plt
from itertools import cycle
from tqdm import tqdm


class Plot:
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = cycle(prop_cycle.by_key()['color'])
    def __init__(self, nbins, xmin, xmax, func, **hist_args):
        self.func = func
        self.hist = hist.Hist.new.Regular(nbins, xmin, xmax, name=hist_args['name']).Weight()
        self.hist_args = hist_args

    def analyze(self, event):
        self.hist.fill(self.func(event))

    def plot(self):
        fig, ax = plt.subplots(figsize=(6,4))
        self.hist.plot1d(ax=ax, ls=self.hist_args.get('ls', '-'),
                         color=self.hist_args.get('color', next(self.colors)))
        plt.show()


def multiplicity(event):
    nucleons = [p for p in event.particles if p.status == 1 and p.pid == 2212]
    return len(nucleons)


def main():
    parser = argparse.ArgumentParser(
            prog='CascadeAnalysis',
            description='Performs basic cascade analysis on a set of NuHepMC events')
    parser.add_argument('--datasets', nargs='+',
                        help='''List of datafiles to read with optional Title argument.
                                i.e. --datasets achilles_dune_numu_geant.hepmc.gz:Title="Achilles Geant"''')
    args = parser.parse_args()

    for dataset in args.datasets:
        dataset_args = dataset.split(':')
        filename = dataset_args[0]
        options = None
        mult_plot = Plot(11, -0.5, 10.5, multiplicity, name='Proton Multiplicity')
        if len(dataset_args) > 1:
            options = dataset_args[1:]
        print(filename, options)
        with pyhepmc.open(filename) as file:
            for event in tqdm(file):
                mult_plot.analyze(event)

    mult_plot.plot()


if __name__ == "__main__":
    main()
