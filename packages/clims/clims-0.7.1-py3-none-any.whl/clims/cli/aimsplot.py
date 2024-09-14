import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import click
from ase.io import read
from clims.read_dos_data import read_species_dos, read_total_dos, get_dos_groups
from clims.read_band_data import read_bands
from clims.read_control import read_control
from clims.plot_mulliken import plot_mulliken_bands, get_groups_for_projections
from clims.cli.citations import cite_and_print

# from time import time

l_numbers = {"s": 0, "p": 1, "d": 2, "f": 3, "g": 4, "h": 5}
l_marker = ["s", "o", "d", "x", "+", "p"]


@click.command()
@click.option(
    "--emin",
    type=float,
    default=-20.1,
    help="Minimum energy value on the y axis of the plot(s).",
)
@click.option(
    "--emax",
    type=float,
    default=5.1,
    help="Maximum energy value on the y axis of the plot(s).",
)
@click.option(
    "--legend_offset",
    type=(float, float),
    default=None,
    nargs=2,
    help="A x, y offset on the canvas that allows one to shift the legend horizontally.",
)
@click.option("--no_legend", is_flag=True, help="No legend will be printed into the plot.")
@click.option(
    "--show_l_components",
    is_flag=True,
    help="L components of the species_dos will be plotted if available.",
)
@click.option(
    "--species",
    type=str,
    help="Comma-separated list of species groups to plot for the Mulliken projection. The L-projection can be enabled by :l, e.g. --species 'Ga P, As :s'",
)
@click.option(
    "--atoms",
    type=str,
    help="Comma-separated list of atom groups to plot for the Mulliken projection. The L-projection can be enabled by :l, e.g. --atoms '1 2:s'",
)
@click.option(
    "--colors",
    type=str,
    help="Comma-separated list of colors for each defined group. Number of colors must match the number of groups.",
)
@click.option(
    "--bands_plot/--no-bands_plot", default=True, help="Plot/Do not plot Band structure."
)
@click.option(
    "--bands_only", is_flag=True, help="Plot band structure without Mulliken projection."
)
@click.option("--dos_plot/--no-dos_plot", default=True, help="Plot/Do not plot DOS.")
@click.option("--save_only", is_flag=True, help="Only save file.")
@click.option(
    "--fontsize", type=int, default=14, help="Define font size for labels and tick marks."
)
@click.option(
    "--linewidth", type=int, default=1, help="Define line width for band and dos lines."
)
@click.option(
    "--maxdos_output", type=float, default=-1, help="The maximum value of the DOS axis."
)
@click.option(
    "--scale_mulliken_marker",
    type=float,
    default=1,
    help="Scales the marker size in the Mulliken-projected band plot.",
)
def aimsplot(
    emin,
    emax,
    legend_offset,
    no_legend,
    show_l_components,
    species,
    atoms,
    colors,
    bands_plot,
    bands_only,
    dos_plot,
    save_only,
    fontsize,
    linewidth,
    maxdos_output,
    scale_mulliken_marker,
):
    """
    Script to plot band structure and DOS calculated with FHI-aims.
    Requires the control.in/geometry.in files as well as the output
    of the calculation to be in the directory from which the script is called.

    This plot will be created in the same directory as a file aimsplot.png if all goes well.
    Specifically, the script allows to create a plot of

    - Energy band structures                  ("output band ...")

    - Density of states                       ("output dos ...")

    - Species-projected densities of states   ("output species_proj_dos ...")
    as well as, optionally, a decomposition of the DOS into angular momentum components

    - and, alternatively, the tetrahedron-integrated versions of DOS and species-projected DOS

    This script can be called simply as "clims-aimsplot", in which case a default range will be used for
    for the energy range covered on the y axis.

    There are several options that allow one to customize the energy range, type of output,
    legend placement etc.
    There are several options that allow one to customize the energy range, type of output,
    legend placement etc.

    clims-aimsplot --help

    provides an overview of the available options.

    For example,

    clims-aimsplot --emin -20. --emax 10. --legend_offset 1.0 0.2

    will customize both the y axis range shown, as well as the placement of the legend in
    the graph.

    To achieve labelling of the special points along the band structure plot,
    add two arguments to the "output band"
    command in the control.in, using the following syntax:

    output band <start> <end> <npoints> <starting_point_name> <ending_point_name>

    Example: To plot a band with 20 points from Gamma to half way along one of the
           reciprocal lattice vectors, write (in control.in)

    output band 0.0 0.0 0.0 0.5 0.0 0.0 20 Gamma <End_point_name>

    For species-projected DOS and Mulliken-projected band structure plots, it is also
    possible to define individual groups of either species or atoms and optionally assign
    individual colors to the groups. The syntax for the species works as follows:

    clims-aimsplot --species "Pb I, H N C" --colors "blue, green"

    This will create two groups of projections: One for Pb and I, and another for H, N, C. The
    order of the groups also defines the plot order.
    """

    ###########
    # OPTIONS #
    ###########
    # The DPI used for printing out images
    print_resolution = 250
    # Turn on spline interpolation for band structures NOT VERY WELL TESTED!
    # should_spline = False
    # Whether to output the x-axis (e.g. the e=0 line) or not
    output_x_axis = True
    # If spline interpolation turned on, the sampling factor (1 is the original grid)
    # spline_factor = 10

    e_shift = 0

    matplotlib.rcParams["lines.linewidth"] = linewidth
    matplotlib.rcParams["savefig.dpi"] = print_resolution
    matplotlib.rcParams["font.size"] = fontsize

    ########################

    print("Plotting bands for FHI-aims!")
    print("============================\n")
    print("Reading lattice vectors from geometry.in ...")

    structure = read("geometry.in")
    n_atoms = len(structure)
    latvec = structure.get_cell()
    print("Lattice vectors:")
    print(latvec[:], "\n")

    rlatvec = 2.0 * np.pi * latvec.reciprocal()
    print("Reciprocal lattice vectors:")
    print(rlatvec, "\n")

    ########################

    print("Reading information from control.in ...")

    PLOT_BANDS = False
    PLOT_GW = False
    PLOT_BANDS_MULLIKEN = False
    PLOT_DOS = False
    PLOT_DOS_SPECIES = False
    PLOT_DOS_ATOM = False
    PLOT_SOC = False  # This is needed because there will only be one "spin" channel output,
    # but collinear spin may (or may not) be turned on, so the "spin
    # collinear" setting needs to be overridden
    PLOT_DOS_REVERSED = False

    max_spin_channel = 1
    band_segments = []
    band_totlength = 0.0  # total length of all band segments

    try:
        control = read_control()
    except:
        print("Something went wrong while parsing control.in")
        print("The following may missing: control.in or output flags")
        raise

    if atoms and species:
        print("\nPlease specify either '--species' or '--atoms'. Stopping.\n")
        return

    l_index = 0
    if not species and not atoms:
        species = [[s] for s in control["species"].keys()]
        atoms = None
    elif atoms:
        species = None
        if len(atoms.split(":")) == 2:
            atoms, l = atoms.split(":")
            l = l.strip()
            print(f"Plotting atom-projected Output on '{l}'-orbital")
            try:
                l_index = l_numbers[l] + 1
            except KeyError:
                print(
                    f"\nl quantum number '{l}' not in the list {list(l_numbers.keys())}. Stopping.\n"
                )
                return
        elif len(atoms.split(":")) > 2:
            print("Error: Only one l-projection for all groups allowed. Stopping.")
            return
        atoms = atoms.split(",")
        if len(atoms) > 1:
            atoms_tmp = []
            for a in atoms:
                atoms_tmp += [[int(x) for x in a.strip().split()]]
            atoms = atoms_tmp
        else:
            atoms = np.array([atoms[0].split()], dtype=int)
        if max(max(atoms)) > len(structure):
            print("One of your atom number is too big. Stopping.")
            return
    else:
        if len(species.split(":")) == 2:
            species, l = species.split(":")
            l = l.strip()
            print(f"Plotting species-projected Output on '{l}'-orbital")
            try:
                l_index = l_numbers[l] + 1
            except KeyError:
                print(f"l quantum number '{l}' not in the list {list(l_numbers.keys())}")
                return
        elif len(species.split(":")) > 2:
            print("Error: Only one l-projection for all groups allowed. Stopping.")
            return
        species = species.split(",")
        if len(species) > 1:
            species = [s.split() for s in species]
        else:
            species = [species[0].split()]
        atoms = None

    output = control["output"]

    if "spin" in control and control["spin"] == "collinear":
        max_spin_channel = 2

    if (
        "calculate_perturbative_soc" in control
        or "include_spin_orbit" in control
        or "include_spin_orbit_sc" in control
    ):
        PLOT_SOC = True
        max_spin_channel = 1

    if "qpe_calc" in control and control["qpe_calc"] == "gw_expt":
        PLOT_GW = True

    if "bands" in output and bands_plot:
        PLOT_BANDS = True
        if "is_band_mulliken" in output and not bands_only:
            PLOT_BANDS_MULLIKEN = True

        for band in output["bands"]:
            start = np.asarray(band[:3], dtype=float)
            end = np.asarray(band[3:6], dtype=float)
            length = np.linalg.norm(np.dot(end, rlatvec) - np.dot(start, rlatvec))
            band_totlength += length
            npoint = int(band[6])
            startname, endname = "", ""
            if len(band) > 7:
                startname = band[7]
            if len(band) > 8:
                endname = band[8]
            band_segments += [(start, end, length, npoint, startname, endname)]

    if ("dos" in output or "dos_tetrahedron" in output) and dos_plot:
        PLOT_DOS = True

    if (
        ("species_proj_dos" in output or "species_proj_dos_tetrahedron" in output)
        and atoms is None
        and dos_plot
    ):
        PLOT_DOS_SPECIES = True

    if "atom_proj_dos" in output or "atom_proj_dos_tetrahedron" in output:
        PLOT_DOS_ATOM = True

    if PLOT_BANDS_MULLIKEN or PLOT_DOS_SPECIES:
        groups, group_colors, masks = get_groups_for_projections(
            PLOT_SOC, species, atoms, structure, colors
        )

    if PLOT_BANDS and (PLOT_DOS or PLOT_DOS_SPECIES):
        fig, (ax_bands, ax_dos) = plt.subplots(
            nrows=1, ncols=2, layout="tight", sharey=True, width_ratios=[3, 1]
        )
        # ax_bands = plt.axes([0.1, 0.1, 0.6, 0.8])
        # ax_dos = plt.axes([0.72, 0.1, 0.2, 0.8], sharey=ax_bands)
        ax_dos.set_title("DOS")
        plt.setp(ax_dos.get_yticklabels(), visible=False)
        ax_bands.set_ylabel("Energy (eV)")
        PLOT_DOS_REVERSED = True
        plt.setp(ax_bands.spines.values(), lw=2)
        plt.setp(ax_dos.spines.values(), lw=2)
    elif PLOT_BANDS:
        fig, ax_bands = plt.subplots(nrows=1, ncols=1, layout="tight")
        ax_bands.set_ylabel("Energy (eV)")
        plt.setp(ax_bands.spines.values(), lw=2)
    elif PLOT_DOS or PLOT_DOS_SPECIES:
        fig, ax_dos = plt.subplots(nrows=1, ncols=1, layout="tight")
        ax_dos.set_ylabel("DOS")
        plt.setp(ax_dos.spines.values(), lw=2)

    #######################

    if PLOT_BANDS:
        print("Plotting %i band segments..." % len(band_segments))

        if output_x_axis:
            ax_bands.axhline(0, color=(0.0, 0.0, 0.0), linestyle=":")

        band_data, labels, e_shift = read_bands(
            band_segments, band_totlength, max_spin_channel, PLOT_GW
        )
        # start = time()
        for iband, segment in enumerate(band_data.values()):
            for spin in range(max_spin_channel):
                sb = segment[spin]
                ax_bands.plot(sb["xvals"], sb["band_energies"], color=sb["color"])
                if PLOT_BANDS_MULLIKEN:
                    filename = "bandmlk%i%03i.out" % (spin + 1, iband + 1)
                    scatters = plot_mulliken_bands(
                        filename,
                        ax_bands,
                        n_atoms,
                        l_index,
                        PLOT_SOC,
                        sb,
                        masks,
                        groups,
                        group_colors,
                        scale_mulliken_marker,
                    )
        # end = time()
        # print("Timing", end - start)

        if PLOT_BANDS_MULLIKEN and not no_legend:
            lg = ax_bands.legend(
                scatters,
                groups,
                scatterpoints=1,
                fontsize=fontsize,
                loc="lower right",
                bbox_to_anchor=legend_offset,
            )
            for lh in lg.legend_handles:
                lh.set_alpha(1)
                lh.set_sizes([100])

        tickx, tickl = [], []
        for xpos, l in labels:
            ax_bands.axvline(xpos, color="k", linestyle=":")
            tickx += [xpos]
            if l == "Gamma" or l == "G":
                l = "$\\Gamma$"
            tickl += [l]
            print("| %8.3f %s" % (xpos, repr(l)))

        ax_bands.set_xlim(labels[0][0], labels[-1][0])
        ax_bands.set_xticks(tickx)
        ax_bands.set_xticklabels(tickl)
        ax_bands.set_ylim(emin, emax)

    #######################
    maxdos = 0.0
    energy_lim = [100000, -100000]

    if PLOT_DOS_SPECIES:
        dos_species = read_species_dos(list(control["species"].keys()), max_spin_channel)
        dos_groups = get_dos_groups(groups, dos_species, max_spin_channel)
        maxdos = dos_species["maxdos"]
        energy_lim = dos_species["energy_lim"]

    if PLOT_DOS:
        energy, dos, maxdos, energy_lim = read_total_dos()

    spinsgns = [1.0]
    spinlabels = [""]
    if max_spin_channel == 2:
        spinsgns = [1.0, -1.0]
        spinlabels = ["up", "down"]

    if PLOT_DOS_REVERSED:
        ax_dos.axhline(0, color=(1.0, 0.0, 0.0), linestyle=":")
        ax_dos.axvline(0, color=(0.5, 0.5, 0.5))

        if PLOT_DOS:
            for ispin in range(max_spin_channel):
                ax_dos.plot(dos[:, ispin] * spinsgns[ispin], energy + e_shift, color="k")

        if PLOT_DOS_SPECIES:
            for c, s in zip(group_colors, groups):
                for ispin, (spinsgn, spinlabel) in enumerate(zip(spinsgns, spinlabels)):
                    s_energy = dos_groups["x"]
                    species_dos = dos_groups[s][ispin][:, 0]
                    ax_dos.plot(
                        species_dos * spinsgn,
                        s_energy + e_shift,
                        linestyle="-",
                        label=f"{s} {spinlabel}",
                        color=c,
                    )
                    if show_l_components:
                        l_dos = dos_groups[s][ispin][:, 1:]
                        for l in range(l_dos.shape[1]):
                            label = f"{s} (l={l}) {spinlabel}"
                            ax_dos.plot(
                                l_dos[:, l] * spinsgn,
                                s_energy + e_shift,
                                linestyle="--",
                                marker=l_marker[l],
                                markevery=len(s_energy) // 400,
                                label=label,
                                color=c,
                            )

        if maxdos_output > 0:
            # If the user has specified a maximum DOS value, use it
            ax_dos.set_xlim(np.array([min(spinsgns[-1], -0.05), 1.00]) * maxdos_output)
        else:
            # Otherwise use the maximum DOS value read in
            ax_dos.set_xlim(np.array([min(spinsgns[-1], 0.0) - 0.05, 1.05]) * maxdos)

    else:  # not PLOT_DOS_REVERSED
        if PLOT_DOS or PLOT_DOS_SPECIES:
            ax_dos.axvline(0, color="k", ls="--")
            ax_dos.axhline(0, color=(0.5, 0.5, 0.5))
            ax_dos.set_xlabel(r"$\varepsilon - \mu$ (eV)")

        if PLOT_DOS_SPECIES:
            for c, s in zip(group_colors, groups):
                for ispin, (spinsgn, spinlabel) in enumerate(zip(spinsgns, spinlabels)):
                    s_energy = dos_groups["x"]
                    species_dos = dos_groups[s][ispin][:, 0]
                    l_dos = dos_groups[s][ispin][:, 1:]
                    ax_dos.plot(
                        s_energy + e_shift,
                        species_dos * spinsgn,
                        linestyle="-",
                        label=f"{s} {spinlabel}",
                        color=c,
                    )
                    if show_l_components:
                        for l in range(l_dos.shape[1]):
                            label = f"{s} (l={l}) {spinlabel}"
                            ax_dos.plot(
                                s_energy + e_shift,
                                l_dos[:, l] * spinsgn,
                                linestyle="--",
                                marker=l_marker[l],
                                markevery=len(s_energy) // 400,
                                label=label,
                                color=c,
                            )

        if PLOT_DOS:
            for ispin in range(max_spin_channel):
                ax_dos.plot(
                    energy + e_shift, dos[:, ispin] * spinsgns[ispin], label="Total DOS"
                )

            ax_dos.set_xlim(energy[0], energy[-1])
            ax_dos.set_xlim(emin, emax)
            if maxdos_output > 0:
                # If the user has specified a maximum DOS value, use that instead
                ax_dos.set_ylim(np.array([min(spinsgns[-1], -0.05), 1.00]) * maxdos_output)
            else:
                # Otherwise use the maximum DOS value read in
                ax_dos.set_ylim(np.array([min(spinsgns[-1], 0.0) - 0.05, 1.05]) * maxdos)

    if PLOT_DOS_SPECIES and not PLOT_BANDS_MULLIKEN:
        if not no_legend:
            ax_dos.legend(bbox_to_anchor=legend_offset, loc="upper left")

    #######################

    print(
        f"\nThe resolution for saving figures is set to {matplotlib.rcParams['savefig.dpi']} dpi."
    )

    cite_and_print(["aims"])

    def on_q_exit(event):
        if event.key == "q":
            sys.exit(0)

    plt.connect("key_press_event", on_q_exit)
    if save_only:
        plt.savefig("aimsplot.png")
    else:
        plt.show()
