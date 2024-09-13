# coding: utf-8
"""Interface to the win input file used by Wannier90."""
from __future__ import annotations

import numpy as np

from collections import OrderedDict
from abipy.core.mixins import Has_Structure
from abipy.core.structure import Structure
from abipy.abio.variable import InputVariable
from abipy.abio.inputs import AbstractInput
#from abipy.tools.typing import Figure

import abipy.core.abinit_units as abu


def structure2wannier90(structure, units="Bohr") -> str:
    """
    Return string with stucture in wannier90 format.
    """
    if not structure.is_ordered:
        raise NotImplementedError("""\
Received disordered structure with partial occupancies that cannot be converted into a Wannier90 input
Please use OrderDisorderedStructureTransformation or EnumerateStructureTransformation
to build an appropriate supercell from partial occupancies or alternatively use the Virtual Crystal Approximation.""")

    lines = []; app = lines.append

    # Write lattice vectors.
    # Set small values to zero. This usually happens when the CIF file
    # does not give structure parameters with enough digits.
    if units == "Bohr":
        fact = abu.Ang_Bohr
        app("begin unit_cell_cart\nBohr")
    elif units == "Ang":
        fact = 1.0
        app("begin unit_cell_cart\nAng")
    else:
        raise ValueError(f"Invalid {units =}")

    for r in np.where(np.abs(structure.lattice.matrix) > 1e-8, structure.lattice.matrix, 0.0):
        r = r * fact
        app("    %.10f %.10f %.10f" % (r[0], r[1], r[2]))
    app("end unit_cell_cart\n")
    app("begin atoms_frac")
    for site in structure:
        fc = np.where(np.abs(site.frac_coords) > 1e-8, site.frac_coords, 0.0)
        app("%s    %.10f %.10f %.10f" % (site.specie.symbol, fc[0], fc[1], fc[2]))
    app("end atoms_frac\n")

    return "\n".join(lines)


class Wannier90Input(AbstractInput, Has_Structure):
    """
    This object stores the wannier90 input variables.

    .. rubric:: Inheritance Diagram
    .. inheritance-diagram:: Wannier90Input
    """
    @classmethod
    def from_abinit_file(cls, filepath: str) -> Wannier90Input:
        """
        Build wannier90 template input file from Abinit input/output file.
        Possibly with electron bands.
        """
        from abipy import abilab
        with abilab.abiopen(filepath) as abifile:
            new = cls(abifile.structure, comment="Automatically generated by AbiPy %s" % abilab.__version__)
            new.set_vars(num_wann="??", num_bands="??", mp_grid="?? ?? ??", _kpoints="?? ?? ??\n?? ?? ??")
            new.set_vars(exclude_bands_="2, 6-8, 12",
                dis_win_min_=0.0, dis_win_max_=0.0, dis_froz_min_=0.0, dis_froz_max_=0.0)

            ebands = getattr(abifile, "ebands", None)
            if ebands is not None:
                # If the file has an ebands attributes we can fill some important variables.
                kpoints = abifile.ebands.kpoints
                if not kpoints.ksampling.is_mesh:
                    raise ValueError("wannier90 requires k-point mesh")
                mp_divs, shifts = kpoints.mpdivs_shifts
                if mp_divs is None:
                    raise ValueError("wannier90 cannot handle kptrlatt with non-zero off-diagonal elements")
                if len(shifts) > 1:
                    raise ValueError("Multiple shifts are not supported by wannier90")
                # TODO: shifts, check abinit tests.
                #for ($x=0; $x<$ARGV[0]; $x++) {
                #    for ($y=0; $y<$ARGV[1]; $y++) {
                #        for ($z=0; $z<$ARGV[2]; $z++) {
                #            printf ("%12.8f%12.8f%12.8f%14.6e \n", $x/$ARGV[0],$y/$ARGV[1],$z/$ARGV[2],1/$totpts);

                new.set_vars(num_bands=ebands.mband, mp_grid=mp_divs,
                             _kpoints="?? ?? ??\n?? ?? ??")
                if ebands.nsppol == 2: new.set_vars(spin="up")

            new.set_kpath()
            return new

    def __init__(self, structure, comment="", win_args=None, win_kwargs=None, spell_check=True):

        """
        Args:
            structure: |Structure| object
            comment: Optional string with a comment that will be placed at the beginning of the file.
            win_args: List of tuples (key, value) with wannier90 input variables (default: empty)
            win_kwargs: Dictionary with wannier90 input variables (default: empty)
            spell_check: False to disable spell checking for input variables.
        """
        self.set_spell_check(spell_check)
        self._structure = structure
        self.comment = comment

        win_args = [] if win_args is None else win_args
        for key, value in win_args:
            self._check_varname(key)

        win_kwargs = {} if win_kwargs is None else win_kwargs
        for key in win_kwargs:
            self._check_varname(key)

        args = list(win_args)[:]
        args.extend(list(win_kwargs.items()))

        self._vars = OrderedDict(args)

    @property
    def vars(self) ->dict:
        return self._vars

    # This stufff should be moved to the ABC
    def set_spell_check(self, false_or_true) -> None:
        """Activate/Deactivate spell-checking"""
        self._spell_check = bool(false_or_true)

    @property
    def spell_check(self) -> bool:
        """True if spell checking is activated."""
        try:
            return self._spell_check
        except AttributeError: # This is to maintain compatibility with pickle
            return False

    def _check_varname(self, key: str):
        return
        # TODO
        #if not is_wannier90_var(key) and self.spell_check:
        #    raise ValueError("%s is not a registered Wannier90 variable\n"
        #                     "If you are sure the name is correct, please contact the abipy developers\n"
        #                     "or use input.set_spell_check(False)\n" % key)

    @property
    def structure(self) -> Structure:
        """|Structure| object."""
        return self._structure

    def to_string(self, sortmode=None, mode="text", verbose=0) -> str:
        """
        String representation.

        Args:
            sortmode: "a" for alphabetical order, None if no sorting is wanted
            mode: Either `text` or `html` if HTML output with links is wanted.
        """
        lines = []; app = lines.append

        if self.comment:
            app("# " + self.comment.replace("\n", "\n#"))

        if sortmode is None:
            # no sorting.
            keys = self.keys()
        elif sortmode == "a":
            # alphabetical order.
            keys = sorted(self.keys())
        else:
            raise ValueError("Unsupported value for sortmode %s" % str(sortmode))

        app(structure2wannier90(self.structure))

        #root = "https://www.abinit.org/doc/helpfiles/for-v8.4/users/anaddb_help.html"
        for varname in keys:
            value = self[varname]
            #if mode == "html": varname = root + "#%s" % varname
            pre = varname.startswith("_")
            post = varname.endswith("_")
            if not pre and not post:
                app(str(InputVariable(varname, value)))
            else:
                # Special treatment required by arrays (starting with _) and/or
                # commented variables (ending with _)
                if pre: varname = varname[1:]
                if post: varname = varname[:-1]
                c = "#" if post else ""
                if pre: app("%sbegin %s" % (c, varname))
                svar = str(InputVariable("" if pre else "#%s" % varname, value))
                if post: s = "\n".join("#%s" % s for s in svar.split())
                app(svar)
                if pre: app("%send %s" % (c, varname))

            app("")

        return "\n".join(lines) if mode == "text" else "\n".join(lines).replace("\n", "<br>")

    def _repr_html_(self):
        """Integration with jupyter_ notebooks."""
        return self.to_string(mode="html")

    def set_kpath(self, bands_num_points=100, qptbounds=None):
        """
        Set the variables for the computation of the electronic band structure.

        Args:
            bands_num_points: The number of points along the first section of the bandstructure plot
                given by kpoint_path. Other sections will have the same density of k-points
            qptbounds: q-points defining the path in k-space.
                If None, we use the default high-symmetry k-path defined in the pymatgen database.
        """
        #if qptbounds is None: qptbounds = self.structure.calc_kptbounds()
        #qptbounds = np.reshape(qptbounds, (-1, 3))
        lines = []; app = lines.append
        for i, kstart in enumerate(self.structure.hsym_kpoints[:-1]):
            kstop = self.structure.hsym_kpoints[i+1]
            app("%s %.5f %.5f %.5f   %s %.5f %.5f %.5f" % (
                kstart.name, kstart.frac_coords[0], kstart.frac_coords[1], kstart.frac_coords[2],
                kstop.name, kstop.frac_coords[0], kstop.frac_coords[1], kstop.frac_coords[2]))

        return self.set_vars(bands_plot_=False, _kpoint_path="\n".join(lines), bands_num_points=bands_num_points)


# Based on the official documentation at <http://www.wannier.org/doc/user_guide.pdf>
# Section_name : {(varname, type, docstring), (...)}
#_VARS_DATABASE = {
#"System": {
#integer ::
#("num_wann"
#"Number of WF to be found. No default."
#
#"num_bands"
#integer ::
#"Total number of bands passed to the code in the seedname.mmn file. Default num_bands=num_wann"
#
#"unit_cell_cart"
#"""
#The cell lattice vectors should be specified in Cartesian coordinates.
#begin unit_cell_cart
#[units]
#    A1x A1y A1z
#    A2x A2y A2z
#    A3x A3y A3z
#end unit_cell_cart
#
#Here A1x is the x-component of the first lattice vector A1, A2y is the y-component of the second lattice vector A2, etc.
#[units] specifies the units in which the lattice vectors are defined: either Bohr or Ang.
#The default value is Ang.
#"""
#
#"atoms_cart"
#
#The ionic positions may be specified in fractional coordinates relative to the lattice vectors of the unit
#cell, or in absolute Cartesian coordinates. Only one of atoms_cart and atoms_frac may be given in the input file.
#Cartesian coordinates
#begin atoms_cart
#[units]
#end atoms_cart
#
#Fractional coordinates
#begin atoms_frac
#P F P
#1 F
#P
#2 F
#P
#3
#Q F Q
#1 F
#Q
#2 F
#Q
#3
#.
#.
#.
#end atoms_frac
#The first entry on a line is the atomic symbol. The next three entries are the atom’s position in
#fractional coordinates F = F1A1 + F2A2 + F3A3 relative to the cell lattice vectors Ai , i ∈ [1, 3].
#2.4.5 integer, dimension :: mp_grid(3)
#Dimensions of the regular (Monkhorst-Pack) k-point mesh.
#For example, for a 2 × 2 × 2 grid:
#
#    mp_grid : 2 2 2
#
#No default.
