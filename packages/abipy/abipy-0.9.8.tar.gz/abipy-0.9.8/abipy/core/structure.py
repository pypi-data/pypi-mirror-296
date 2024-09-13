# coding: utf-8
"""
This module defines basic objects representing the crystalline structure.
"""
from __future__ import annotations

import sys
import os
import collections
import tempfile
import numpy as np
import pandas as pd
import pickle
import pymatgen.core.units as pmg_units

from pprint import pformat
from collections import OrderedDict
from typing import Any
from monty.collections import AttrDict, dict2namedtuple
from monty.functools import lazy_property
from monty.string import is_string, marquee, list_strings
from monty.termcolor import cprint
#from monty.dev import deprecated
from pymatgen.core.structure import Structure as pmg_Structure
from pymatgen.core.sites import PeriodicSite
from pymatgen.core.lattice import Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from abipy.core.mixins import NotebookWriter
from abipy.core.symmetries import AbinitSpaceGroup
from abipy.tools.plotting import add_fig_kwargs, get_ax_fig_plt, get_axarray_fig_plt, add_plotly_fig_kwargs
from abipy.iotools import as_etsfreader, Visualizer
from abipy.tools.typing import Figure


__all__ = [
    "mp_match_structure",
    "mp_search",
    "cod_search",
    "Structure",
    "dataframes_from_structures",
]


def mp_match_structure(obj):
    """
    Finds matching structures on the Materials Project database.

    Args:
        obj: filename or |Structure| object.
        final (bool): Whether to get the final structure, or the initial
            (pre-relaxation) structure. Defaults to True.

    Returns:
        :class:`MpStructures` object with
            structures: List of matching structures and list of Materials Project identifier.
    """
    structure = Structure.as_structure(obj)
    # Must use pymatgen structure else server does not know how to handle the JSON doc.
    structure.__class__ = pmg_Structure

    from abipy.core import restapi
    structures, mpids = [], []
    with restapi.get_mprester() as rest:
        try:
            if getattr(rest, "get_data") is None:
                raise RuntimeError("mp_match_structure requires mp-api, please install it with `pip install mp-api`")

            mpids = rest.find_structure(structure)
            if mpids:
                structures = [Structure.from_mpid(mid) for mid in mpids]

        except Exception as exc:
            cprint(str(exc), "red")

        finally:
            # Back to abipy structure
            structure = Structure.as_structure(structure)
            structures.insert(0, structure)
            mpids.insert(0, "this")
            return restapi.MpStructures(structures=structures, ids=mpids)


def mp_search(chemsys_formula_id):
    """
    Connect to the materials project database.
    Get a list of structures corresponding to a chemical system, formula, or materials_id.

    Args:
        chemsys_formula_id (str): A chemical system (e.g., Li-Fe-O),
            or formula (e.g., Fe2O3) or materials_id (e.g., mp-1234).

    Returns:
        :class:`MpStructures` object with
            List of Structure objects, Materials project ids associated to structures.
            and List of dictionaries with MP data (same order as structures).

        Note that the attributes evalute to False if no match is found.
    """
    chemsys_formula_id = chemsys_formula_id.replace(" ", "")

    structures, mpids, data = [], [], None
    from abipy.core import restapi
    from pymatgen.ext.matproj import MPRestError
    with restapi.get_mprester() as rest:
        try:
            if getattr(rest, "get_data") is None:
                raise RuntimeError("mp_search requires mp-api, please install it with `pip install mp-api`")

            data = rest.get_data(chemsys_formula_id, prop="")
            if data:
                structures = [Structure.from_str(d["cif"], fmt="cif", primitive=False, sort=False) for d in data]
                mpids = [d["material_id"] for d in data]
                # Want AbiPy structure.
                structures = list(map(Structure.as_structure, structures))

        except MPRestError:
            cprint(str(exc), "magenta")

        return restapi.MpStructures(structures, mpids, data=data)


def cod_search(formula, primitive=False):
    """
    Connect to the COD_ database. Get list of structures corresponding to a chemical formula

    Args:
        formula (str): Chemical formula (e.g., Fe2O3)
        primitive (bool): True if primitive structures are wanted. Note that many COD structures are not primitive.

    Returns:
        :class:`CodStructures` object with
            List of Structure objects, COD ids associated to structures.
            and List of dictionaries with COD data (same order as structures).

        Note that the attributes evalute to False if no match is found
    """
    from pymatgen.ext.cod import COD
    data = COD().get_structure_by_formula(formula)

    cod_ids = [e.pop("cod_id") for e in data]
    # Want AbiPy structure.
    structures = list(map(Structure.as_structure, [e.pop("structure") for e in data]))
    if primitive:
        structures = [s.get_primitive_structure() for s in structures]

    from abipy.core import restapi
    return restapi.CodStructures(structures, cod_ids, data=data)


def display_structure(obj, **kwargs):
    """
    Use Jsmol to display a structure in the jupyter notebook.
    Requires `nbjsmol` notebook extension installed on the local machine.
    Install it with `pip install nbjsmol`. See also https://github.com/gmatteo/nbjsmol.

    Args:
        obj: Structure object or file with a structure or python object with a `structure` attribute.
        kwargs: Keyword arguments passed to `nbjsmol_display`
    """
    try:
        from nbjsmol import nbjsmol_display
    except ImportError as exc:
        raise ImportError(str(exc) +
                          "\ndisplay structure requires nbjsmol package\n."
                          "Install it with `pip install nbjsmol.`\n"
                          "See also https://github.com/gmatteo/nbjsmol.")

    # Cast to structure, get string with cif data and pass it to nbjsmol.
    structure = Structure.as_structure(obj)
    return nbjsmol_display(structure.to(fmt="cif"), ext=".cif", **kwargs)


def get_structures_from_file(filepath: PathLike, index) -> list[Structure]:
    """
    """
    #if index is None:
    #    index = -1

    if filepath.endswith(".traj"):
        # ASE trajectory file.
        from ase.atoms import Atoms
        from ase.io import read
        atoms_list = read(filepath, index=index)
        if not isinstance(atoms_list, list):
            assert isinstance(atoms_list, Atoms)
            atoms_list = [atoms_list]

    # TODO: HIST.nc and XDATCAR
    #elif filepath.endswith("_HIST.nc"):
    #    from abipy.dynamics.hist import HistFile
    #    with HistFile(filepath) as hist:
    #        return hist.read_structures(index)

    #elif filepath.endswith("XDATCAR"):

    else:
        raise NotImplementedError(f"Don't know how to extract structures with index from {filepath=}")

    return [Structure.as_structure(atoms) for atoms in atoms_list]


def get_first_and_last_structure_from_file(filepath: PathLike) -> tuple[Structure]:
    """
    Helper function to read the first and the last structure from a trajectory file.
    Simplified wrapper around get_structures_from_file.
    """
    first_structure = get_structures_from_file(filepath, index=0)[0]
    last_structure = get_structures_from_file(filepath, index=-1)[0]
    return first_structure, last_structure


class Structure(pmg_Structure, NotebookWriter):
    """
    Extends :class:`pymatgen.core.structure.Structure` with Abinit-specific methods.

    .. rubric:: Inheritance Diagram
    .. inheritance-diagram:: Structure
    """

    @classmethod
    def as_structure(cls, obj: Any) -> Structure:
        """
        Convert obj into a |Structure|. Accepts:

            - Structure object.
            - Filename
            - Dictionaries (JSON_ format or dictionaries with abinit variables).
            - Objects with a ``structure`` attribute.
            - ASE atoms.
        """
        if isinstance(obj, cls):
            return obj

        if isinstance(obj, pmg_Structure):
            obj.__class__ = cls
            return obj

        if hasattr(obj, "ase_objtype"):
            # ASE Atoms.
            from pymatgen.io.ase import AseAtomsAdaptor
            return AseAtomsAdaptor.get_structure(obj, cls=cls)

        if hasattr(obj, "atoms") and hasattr(obj.atoms, "ase_objtype"):
            # Handle ASE constraints e.g. ExpCellFilter. Note recursive call
            return Structure.as_structure(obj.atoms)

        if is_string(obj):
            return cls.from_file(obj)

        if isinstance(obj, collections.abc.Mapping):
            if "@module" in obj:
                return Structure.from_dict(obj)
            else:
                return Structure.from_abivars(obj)

        if hasattr(obj, "structure"):
            return cls.as_structure(obj.structure)

        elif hasattr(obj, "final_structure"):
            # This for HIST.nc file
            return cls.as_structure(obj.final_structure)

        raise TypeError("Don't know how to convert %s into a structure" % type(obj))

    @classmethod
    def from_file(cls, filepath: str, primitive: bool = False, sort: bool = False) -> Structure:
        """
        Reads a structure from a file. For example, anything ending in
        a "cif" is assumed to be a Crystallographic Information Format file.
        Supported formats include CIF_, POSCAR/CONTCAR, CHGCAR, LOCPOT,
        vasprun.xml, CSSR, Netcdf and pymatgen's JSON serialized structures.

        Netcdf files supported:
            All files produced by ABINIT with info of the crystalline geometry
            HIST.nc, in this case the last structure of the history is returned.

        Args:
            filename (str): The filename to read from.
            primitive (bool): Whether to convert to a primitive cell
                Only available for cifs, POSCAR, CSSR, JSON, YAML
                Defaults to True.
            sort (bool): Whether to sort sites. Default to False.

        Returns: |Structure| object
        """
        root, ext = os.path.splitext(filepath)

        if filepath.endswith("_HIST.nc"):
            # Abinit history file. In this case we return the last structure!
            # Note that HIST does not follow the etsf-io conventions.
            from abipy.dynamics.hist import HistFile
            with HistFile(filepath) as hist:
                return hist.structures[-1]

        elif filepath.endswith(".nc"):
            # Generic netcdf file.
            ncfile, closeit = as_etsfreader(filepath)

            new = ncfile.read_structure(cls=cls)

            if "space_group" in ncfile.rootgrp.variables:
                new.set_abi_spacegroup(AbinitSpaceGroup.from_ncreader(ncfile))

            # Try to read indsym table from file (added in 8.9.x)
            indsym = ncfile.read_value("indsym", default=None)
            if indsym is not None:
                # Fortran --> C convention
                indsym[:, :, 3] -= 1
                new.indsym = indsym

            if closeit: ncfile.close()

        elif filepath.endswith(".abi") or filepath.endswith(".in"):
            # Abinit input file. Here I assume that the input file contains a single structure.
            from abipy.abio.abivars import AbinitInputFile
            return AbinitInputFile.from_file(filepath).structure

        elif filepath.endswith(".abo") or filepath.endswith(".out"):
            # Abinit output file. We can have multi-datasets and multiple initial/final structures!
            # By design, we return the last structure if out is completed else the initial one.
            # None is returned if the structures are different.
            from abipy.abio.outputs import AbinitOutputFile
            with AbinitOutputFile(filepath) as out:
                #print("initial_structures:\n", out.initial_structures, "\nfinal_structures:\n", out.final_structures)
                if out.final_structures: return out.final_structure
                if out.initial_structures: return out.initial_structure

            raise ValueError("Cannot find structure in Abinit output file `%s`" % filepath)

        elif filepath.endswith(".abivars") or filepath.endswith(".ucell"):
            with open(filepath, "rt") as fh:
                return cls.from_abistring(fh.read())

        elif filepath.endswith("_DDB") or root.endswith("_DDB") or filepath.endswith(".ddb"):
            # DDB file.
            from abipy.abilab import abiopen
            with abiopen(filepath) as abifile:
                return abifile.structure

        elif filepath.endswith(".pickle"):
            # From pickle.
            with open(filepath, "rb") as fh:
                new = pickle.load(fh)
                if not isinstance(new, pmg_Structure):
                    # Is it a object with a structure property?
                    if hasattr(new, "structure"): new = new.structure

                if not isinstance(new, pmg_Structure):
                    raise TypeError("Don't know how to extract a Structure from file %s, received type %s" %
                        (filepath, type(new)))

                if new.__class__ != cls: new.__class__ = cls

        elif filepath.endswith(".xyz"):
            # ASE extended xyz format.
            try:
                from ase.io import read
            except ImportError as exc:
                raise RuntimeError("ase is required to read xyz files. Use `pip install ase`") from exc
            return cls.as_structure(read(filepath))

        else:
            # Invoke pymatgen and change class. Note that AbinitSpacegroup is missing here.
            new = super().from_file(filepath, primitive=primitive, sort=sort)
            if new.__class__ != cls: new.__class__ = cls

        return new

    @classmethod
    def from_mpid(cls, material_id: str) -> Structure:
        """
        Get a Structure corresponding to a material_id.

        Args:
            material_id (str): Materials Project material_id (a string, e.g., mp-1234).
            final (bool): Whether to get the final structure, or the initial
                (pre-relaxation) structure. Defaults to True.

        Returns: |Structure| object.
        """
        material_id = str(material_id)
        if not material_id.startswith("mp-"):
            raise ValueError("Materials project ID should start with mp-")

        # Get pytmatgen structure and convert it to abipy structure
        from abipy.core import restapi
        with restapi.get_mprester() as rest:
            new = rest.get_structure_by_material_id(material_id)
            return cls.as_structure(new)

    @classmethod
    def from_cod_id(cls, cod_id: int, primitive: bool = False, **kwargs) -> Structure:
        """
        Queries the COD_ database for a structure by id. Returns |Structure| object.

        Args:
            cod_id (int): COD id.
            primitive (bool): True if primitive structures are wanted.
                Note that many COD structures are not primitive.
            kwargs: Arguments passed to ``get_structure_by_id``

        Returns: |Structure| object.
        """
        from pymatgen.ext.cod import COD
        new = COD().get_structure_by_id(cod_id, **kwargs)
        if primitive: new = new.get_primitive_structure()
        return cls.as_structure(new)

    @classmethod
    def from_ase_atoms(cls, atoms) -> Structure:
        """
        Returns structure from ASE Atoms.

        Args:
            atoms: ASE Atoms object
        """
        import pymatgen.io.ase as aio
        return aio.AseAtomsAdaptor.get_structure(atoms, cls=cls)

    # FIXME: Temporary workaround to maintain compatbility with old pymatgen versions.
    # m_elems was added in v2024.7.18
    @property
    def n_elems(self) -> int:
        """Number of types of atoms."""
        return len(self.types_of_species)

    def to_ase_atoms(self, calc=None):
        """
        Returns ASE Atoms object from structure and attach calculator calc.
        """
        import pymatgen.io.ase as aio
        atoms = aio.AseAtomsAdaptor.get_atoms(self)
        if calc is not None: atoms.calc = calc
        return atoms

    def get_phonopy_atoms(self):
        """
        Convert a pymatgen Structure object to a PhonopyAtoms object.
        """
        from pymatgen.io.phonopy import get_phonopy_structure
        return get_phonopy_structure(self)

    @classmethod
    def boxed_molecule(cls, pseudos, cart_coords, acell=3 * (10,)) -> Structure:
        """
        Creates a molecule in a periodic box of lengths acell in Bohr.

        Args:
            pseudos: List of pseudopotentials
            cart_coords: Cartesian coordinates
            acell: Lengths of the box in *Bohr*
        """
        from pymatgen.core.structure import Molecule
        cart_coords = np.atleast_2d(cart_coords)
        molecule = Molecule([p.symbol for p in pseudos], cart_coords)
        l = pmg_units.ArrayWithUnit(acell, "bohr").to("ang")

        new = molecule.get_boxed_structure(l[0], l[1], l[2])
        return cls.as_structure(new)

    @classmethod
    def boxed_atom(cls, pseudo, cart_coords=3*(0,), acell=3*(10,)) -> Structure:
        """
        Creates an atom in a periodic box of lengths acell in Bohr.

        Args:
            pseudo: Pseudopotential object.
            cart_coords: Cartesian coordinates in Angstrom
            acell: Lengths of the box in *Bohr* (Abinit input variable)
        """
        return cls.boxed_molecule([pseudo], cart_coords, acell=acell)

    @classmethod
    def bcc(cls, a, species, primitive=True, units="ang", **kwargs) -> Structure:
        """
        Build a primitive or a conventional bcc crystal structure.

        Args:
            a: Lattice parameter (Angstrom if units is not given)
            species: Chemical species. See __init__ method of |pymatgen-Structure|
            primitive: if True a primitive cell will be produced, otherwise a conventional one
            units: Units of input lattice parameters e.g. "bohr", "pm"
            kwargs: All keyword arguments accepted by |pymatgen-Structure|.
        """
        a = pmg_units.Length(a, units).to("ang")
        if primitive:
            lattice = 0.5 * float(a) * np.array([
                -1,  1,  1,
                 1, -1,  1,
                 1,  1, -1])

            coords = [[0, 0, 0]]

        else:
            lattice = float(a) * np.eye(3)
            coords = [[0, 0, 0],
                      [0.5, 0.5, 0.5]]
            species = np.repeat(species, 2)

        return cls(lattice, species, coords=coords,  **kwargs)

    @classmethod
    def fcc(cls, a: float, species, primitive=True, units="ang", **kwargs) -> Structure:
        """
        Build a primitive or a conventional fcc crystal structure.

        Args:
            a: Lattice parameter (Angstrom if units is not given)
            species: Chemical species. See __init__ method of :class:`pymatgen.Structure`
            primitive: if True a primitive cell will be produced, otherwise a conventional one
            units: Units of input lattice parameters e.g. "bohr", "pm"
            kwargs: All keyword arguments accepted by :class:`pymatgen.Structure`
        """
        a = pmg_units.Length(a, units).to("ang")
        if primitive:
            lattice = 0.5 * float(a) * np.array([
                0,  1,  1,
                1,  0,  1,
                1,  1,  0])
            coords = [[0, 0, 0]]
        else:
            lattice = float(a) * np.eye(3)
            species = np.repeat(species, 4)
            coords = [[0, 0, 0],
                      [0.5, 0.5, 0],
                      [0.5, 0, 0.5],
                      [0, 0.5, 0.5]]

        return cls(lattice, species, coords=coords, **kwargs)

    @classmethod
    def zincblende(cls, a, species, units="ang", **kwargs) -> Structure:
        """
        Build a primitive zincblende crystal structure.

        Args:
            a: Lattice parameter (Angstrom if units is not given)
            species: Chemical species. See __init__ method of :class:`pymatgen.Structure`
            units: Units of input lattice parameters e.g. "bohr", "pm"
            kwargs: All keyword arguments accepted by :class:`pymatgen.Structure`

        Example::
            Structure.zincblende(a, ["Zn", "S"])
        """
        a = pmg_units.Length(a, units).to("ang")
        lattice = 0.5 * float(a) * np.array([
            0,  1,  1,
            1,  0,  1,
            1,  1,  0])

        frac_coords = np.reshape([0, 0, 0, 0.25, 0.25, 0.25], (2, 3))
        return cls(lattice, species, frac_coords, coords_are_cartesian=False, **kwargs)

    @classmethod
    def rocksalt(cls, a, species, units="ang", **kwargs) -> Structure:
        """
        Build a primitive fcc crystal structure.

        Args:
            a: Lattice parameter (Angstrom if units is not given)
            units: Units of input lattice parameters e.g. "bohr", "pm"
            species: Chemical species. See __init__ method of :class:`pymatgen.Structure`
            kwargs: All keyword arguments accepted by :class:`pymatgen.Structure`

        Example::
            Structure.rocksalt(a, ["Na", "Cl"])
        """
        a = pmg_units.Length(a, units).to("ang")
        lattice = 0.5 * float(a) * np.array([
            0,  1,  1,
            1,  0,  1,
            1,  1,  0])

        frac_coords = np.reshape([0, 0, 0, 0.5, 0.5, 0.5], (2, 3))
        return cls(lattice, species, frac_coords, coords_are_cartesian=False, **kwargs)

    @classmethod
    def ABO3(cls, a, species, units="ang", **kwargs) -> Structure:
        """
        Peroviskite structures.

        Args:
            a: Lattice parameter (Angstrom if units is not given)
            species: Chemical species. See __init__ method of :class:`pymatgen.Structure`
            units: Units of input lattice parameters e.g. "bohr", "pm"
            kwargs: All keyword arguments accepted by :class:`pymatgen.Structure`
        """
        a = pmg_units.Length(a, units).to("ang")
        lattice = float(a) * np.eye(3)
        frac_coords = np.reshape([
            0,     0,   0,  # A (2a)
            0.5, 0.5, 0.5,  # B (2a)
            0.5, 0.5, 0.0,  # O (6b)
            0.5, 0.0, 0.5,  # O (6b)
            0.0, 0.5, 0.5,  # O (6b)
        ], (5, 3))

        return cls(lattice, species, frac_coords, coords_are_cartesian=False, **kwargs)

    @classmethod
    def from_abistring(cls, string: str) -> Structure:
        """
        Initialize Structure from a string with Abinit input variables.
        """
        from abipy.abio.abivars import AbinitInputFile, structure_from_abistruct_fmt
        if "xred_symbols" not in string:
            # Standard (verbose) input file with znucl, typat etc.
            return AbinitInputFile.from_string(string).structure
        else:
            return structure_from_abistruct_fmt(string)

    @classmethod
    def from_abivars(cls, *args, **kwargs) -> Structure:
        """
        Build a |Structure| object from a dictionary with ABINIT variables.

        Example::

            al_structure = Structure.from_abivars(
                acell=3*[7.5],
                rprim=[0.0, 0.5, 0.5,
                       0.5, 0.0, 0.5,
                       0.5, 0.5, 0.0],
                typat=1,
                xred=[0.0, 0.0, 0.0],
                ntypat=1,
                znucl=13,
            )

        ``xred`` can be replaced with ``xcart`` or ``xangst``.
        """
        from abipy.flowtk.abiobjects import structure_from_abivars
        return structure_from_abivars(cls, *args, **kwargs)

    @property
    def species_by_znucl(self):
        """
        Return list of unique species found in the structure **ordered according to sites**.

        Example:

            Site0: 0.5 0 0 O
            Site1: 0   0 0 Si

        produces [Specie_O, Specie_Si] and not set([Specie_O, Specie_Si]) as in `types_of_specie`.

        Important:: We call this method `species_by_znucl` but this does not mean that the list can automagically
        reproduce the value of `znucl(ntypat)` specified in an **arbitrary** ABINIT input file created by the user.
        This array is ordered as the znucl list produced by AbiPy when writing the structure to the input file.
        """
        from abipy.flowtk.abiobjects import species_by_znucl
        return species_by_znucl(self)

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self, title=None, verbose=0) -> str:
        """
        String representation. Extends the implementation of the superclass.
        """
        lines = []; app = lines.append
        if title is not None: app(marquee(title, mark="="))
        if verbose:
            app(self.spget_summary(verbose=verbose))
        else:
            app(super().__str__())

        if verbose > 1:
            for i, vec in enumerate(self.lattice.matrix):
                app("a_%d: %.8f %.8f %.8f" % (i + 1, vec[0], vec[1], vec[2]))

        if self.abi_spacegroup is not None:
            app("\nAbinit Spacegroup: %s" % self.abi_spacegroup.to_string(verbose=verbose))

        return "\n".join(lines)

    def to(self, fmt=None, filename=None, **kwargs):
        __doc__ = pmg_Structure.to.__doc__ + \
            "\n Accepts also fmt=`abinit` or `abivars` or `.abi` as Abinit input file extension"

        filename = filename or ""
        fmt = "" if fmt is None else fmt.lower()
        fname = os.path.basename(filename)

        if fmt in ("abi", "abivars", "abinit") or fname.endswith(".abi"):
            if filename:
                with open(filename, "wt") as f:
                    f.write(self.abi_string)
            else:
                return self.abi_string
        else:
            return super().to(fmt=fmt, filename=filename, **kwargs)

    def mp_match(self, **kwargs):
        """
        Finds matching structures on the Materials Project database.
        Just a wrapper around mp_match_structure.
        """
        return mp_match_structure(self, **kwargs)

    def write_cif_with_spglib_symms(self, filename, symprec=1e-3, angle_tolerance=5.0,
                                    significant_figures=8,
                                    ret_string=False):
        """
        Write CIF file with symmetries as detected by spglib.

        Args:
            symprec (float): If not none, finds the symmetry of the structure
                and writes the cif with symmetry information. Passes symprec
                to the SpacegroupAnalyzer.
            significant_figures (int): Specifies precision for formatting of floats. Defaults to 8.
            angle_tolerance (float): Angle tolerance for symmetry finding. Passes
                angle_tolerance to the SpacegroupAnalyzer. Used only if symprec is not None.
            ret_string: True to return string.
        """
        from pymatgen.io.cif import CifWriter
        cif_str = str(CifWriter(self,
                      symprec=symprec, significant_figures=significant_figures, angle_tolerance=angle_tolerance,
                      refine_struct=False))

        if not ret_string:
            with open(filename, "wt") as fh:
                fh.write(cif_str)
        else:
            return cif_str

    def __mul__(self, scaling_matrix) -> Structure:
        """
        Makes a supercell. Allowing to have sites outside the unit cell
        See pymatgen for docs.

        Wraps __mul__ operator of pymatgen structure to return abipy structure
        """
        new = super().__mul__(scaling_matrix)
        return self.__class__.as_structure(new)

    __rmul__ = __mul__

    def to_abivars(self, enforce_znucl=None, enforce_typat=None, **kwargs) -> dict:
        """
        Returns a dictionary with the ABINIT variables.

        Args:
            enforce_znucl[ntypat] = Enforce this value for znucl.
            enforce_typat[natom] = Fortran conventions. Start to count from 1.
        """
        from abipy.flowtk.abiobjects import structure_to_abivars
        return structure_to_abivars(self, enforce_znucl=enforce_znucl, enforce_typat=enforce_typat, **kwargs)

    @property
    def latex_formula(self) -> str:
        """LaTeX formatted formula: e.g., Fe2O3 is transformed to Fe$_{2}$O$_{3}$."""
        from pymatgen.util.string import latexify
        return latexify(self.formula)

    @property
    def poscar_string(self) -> str:
        """String with the structure in POSCAR format."""
        return self.to(fmt="POSCAR")

    @property
    def abi_string(self) -> str:
        """String with the ABINIT input associated to this structure."""
        return self.get_abi_string(fmt="abinit_input")

    def get_abi_string(self, fmt: str = "abinit_input") -> str:
        """
        Return a string with the ABINIT input associated to this structure. Two formats are available.
        fmt="abinit_input" corresponds to the standard format with `typat`, `znucl`.
        fmt="abicell" is the lightweight format that uses `xred_symbols`
        This format can be used to include the structure in the input via the structure "abivars:FILE" syntax.
        """
        lines = []
        app = lines.append

        if fmt == "abinit_input":
            from abipy.abio.variable import InputVariable
            abivars = self.to_abivars()
            for varname, value in abivars.items():
                app(str(InputVariable(varname, value)))

            return "\n".join(lines)

        if fmt == "abicell":
            # # MgB2 lattice structure.
            # natom   3
            # acell   2*3.086  3.523 Angstrom
            # rprim   0.866025403784439  0.5  0.0
            #        -0.866025403784439  0.5  0.0
            #         0.0                0.0  1.0

            # # Atomic positions in reduced coordinates followed by element symbol.
            # xred_symbols
            #  0.0  0.0  0.0 Mg
            #  1/3  2/3  0.5 B
            #  2/3  1/3  0.5 B

            rprim = pmg_units.ArrayWithUnit(self.lattice.matrix, "ang").to("bohr")
            #angdeg = structure.lattice.angles
            xred = np.reshape([site.frac_coords for site in self], (-1, 3))

            # Set small values to zero. This usually happens when the CIF file
            # does not give structure parameters with enough digits.
            rprim = np.where(np.abs(rprim) > 1e-8, rprim, 0.0)
            xred = np.where(np.abs(xred) > 1e-8, xred, 0.0)
            symbols = [site.specie.symbol for site in self]

            app(f"# formula: {self.composition.formula}")
            app(f"natom {len(self)}")
            app("acell 1.0 1.0 1.0")
            app("rprim")

            def v_to_s(vec):
                return "%.8f %.8f %.8f" % (vec[0], vec[1], vec[2])

            for avec in rprim:
                app(v_to_s(avec))
            app("# Atomic positions in reduced coordinates followed by element symbol.")
            app("xred_symbols")
            for (frac_coords, symbol) in zip(xred, symbols):
                app(v_to_s(frac_coords) + f" {symbol}")

            return("\n".join(lines))

        raise ValueError(f"Unknown fmt: {fmt}")

    def get_panel(self, with_inputs=True, **kwargs):
        """
        Build panel with widgets to interact with the structure either in a notebook or in a bokeh app.

        Args:
            with_inputs: True if tabs for generating input files should be shown.
        """
        from abipy.panels.structure import StructurePanel
        return StructurePanel(structure=self).get_panel(with_inputs=with_inputs, **kwargs)

    def get_conventional_standard_structure(self, international_monoclinic=True,
                                           symprec=1e-3, angle_tolerance=5) -> Structure:
        """
        Gives a structure with a conventional cell according to certain standards.
        The standards are defined in :cite:`Setyawan2010`
        They basically enforce as much as possible norm(a1) < norm(a2) < norm(a3)

        Returns: The structure in a conventional standardized cell
        """
        spga = SpacegroupAnalyzer(self, symprec=symprec, angle_tolerance=angle_tolerance)
        new = spga.get_conventional_standard_structure(international_monoclinic=international_monoclinic)
        return self.__class__.as_structure(new)

    def abi_primitive(self, symprec=1e-3, angle_tolerance=5, no_idealize=0) -> Structure:
        #TODO: this should be moved to pymatgen in the get_refined_structure or so ... to be considered in February 2016
        import spglib
        from pymatgen.io.ase import AseAtomsAdaptor
        try:
            from ase.atoms import Atoms
        except ImportError:
            raise ImportError('Could not import Atoms from ase. Install it with `conda install ase` or pip')

        s = self.get_sorted_structure()
        ase_adaptor = AseAtomsAdaptor()
        ase_atoms = ase_adaptor.get_atoms(structure=s)

        #standardized = spglib.standardize_cell(ase_atoms, to_primitive=1, no_idealize=no_idealize,
        #                                       symprec=symprec, angle_tolerance=angle_tolerance)

        spglib_cell = (ase_atoms.cell, ase_atoms.get_scaled_positions(), ase_atoms.get_atomic_numbers())
        standardized = spglib.standardize_cell(spglib_cell, to_primitive=1, no_idealize=no_idealize,
                                               symprec=symprec, angle_tolerance=angle_tolerance)

        standardized_ase_atoms = Atoms(scaled_positions=standardized[1], numbers=standardized[2], cell=standardized[0])
        standardized_structure = ase_adaptor.get_structure(standardized_ase_atoms)

        return self.__class__.as_structure(standardized_structure)

    def new_with_uptri_lattice(self, mode="uptri") -> Structure:
        """
        Build and return new structure with cell matrix in upper triangle form.
        In the cell matrix, lattice vectors are along rows.

        Args:
            mode="lowtri" if lower triangle cell matrix is wanted.
        """
        a, b, c = self.lattice.abc
        alpha, beta, gamma = self.lattice.angles

        # vesta = True means that we have a lower triangle lattice matrix (row vectors)
        from pymatgen.core.lattice import Lattice
        lattice = Lattice.from_parameters(a, b, c, alpha, beta, gamma, vesta=True)

        if mode == "lowtri":
            a1, a2, a3 = lattice.matrix
        elif mode =="uptri":
            new_matrix = lattice.matrix.copy()
            for i in range(3):
                new_matrix[i,0] = lattice.matrix[i,2]
                new_matrix[i,2] = lattice.matrix[i,0]
            a1, a2, a3 = new_matrix[2], new_matrix[1], new_matrix[0]
        else:
            raise ValueError(f"Invalid {mode=}")

        from ase.cell import Cell
        atoms = self.to_ase_atoms()
        atoms.set_cell(Cell([a1, a2, a3]), scale_atoms=True)

        return Structure.from_ase_atoms(atoms)

    def refine(self, symprec=1e-3, angle_tolerance=5) -> Structure:
        """
        Get the refined structure based on detected symmetry. The refined
        structure is a *conventional* cell setting with atoms moved to the
        expected symmetry positions.

        Returns: Refined structure.
        """
        sym_finder = SpacegroupAnalyzer(structure=self, symprec=symprec, angle_tolerance=angle_tolerance)
        new = sym_finder.get_refined_structure()
        return self.__class__.as_structure(new)

    def abi_sanitize(self, symprec=1e-3, angle_tolerance=5,
                     primitive=True, primitive_standard=False) -> Structure:
        """
        Returns a new structure in which:

            * Structure is refined.
            * Reduced to primitive settings.
            * Lattice vectors are exchanged if the triple product is negative

        Args:
            symprec (float): Symmetry precision used to refine the structure.
            angle_tolerance (float): Tolerance on angles.
                if ``symprec`` is None and `angle_tolerance` is None, no structure refinement is peformed.
            primitive (bool): Returns most primitive structure found.
            primitive_standard (bool): Whether to convert to a primitive cell using
                the standards defined in Setyawan, W., & Curtarolo, S. (2010).
                High-throughput electronic band structure calculations:
                Challenges and tools. Computational Materials Science, 49(2), 299-312.
                doi:10.1016/j.commatsci.2010.05.010
        """
        from pymatgen.transformations.standard_transformations import PrimitiveCellTransformation, SupercellTransformation
        structure = self.__class__.from_sites(self)

        # Refine structure
        if symprec is not None and angle_tolerance is not None:
            structure = structure.refine(symprec=symprec, angle_tolerance=angle_tolerance)

        # Convert to primitive structure.
        #primitive_standard = False
        if primitive:
            if primitive_standard:
                # Setyawan, W., & Curtarolo, S.
                sym_finder_prim = SpacegroupAnalyzer(structure=structure, symprec=symprec, angle_tolerance=angle_tolerance)
                structure = sym_finder_prim.get_primitive_standard_structure(international_monoclinic=False)
            else:
                # Find most primitive structure.
                get_prim = PrimitiveCellTransformation()
                structure = get_prim.apply_transformation(structure)

        # Exchange last two lattice vectors if triple product is negative.
        m = structure.lattice.matrix
        x_prod = np.dot(np.cross(m[0], m[1]), m[2])
        if x_prod < 0:
            #print("Negative triple product --> exchanging last two lattice vectors.")
            trans = SupercellTransformation(((1, 0, 0), (0, 0, 1), (0, 1, 0)))
            structure = trans.apply_transformation(structure)
            m = structure.lattice.matrix
            x_prod = np.dot(np.cross(m[0], m[1]), m[2])
            if x_prod < 0: raise RuntimeError("x_prod is still negative!")

        return self.__class__.as_structure(structure)

    def get_oxi_state_decorated(self, **kwargs) -> Structure:
        """
        Use :class:`pymatgen.analysis.bond_valence.BVAnalyzer` to estimate oxidation states
        Return oxidation state decorated structure.
        This currently works only for ordered structures only.

        Args:
            kwargs: Arguments passed to BVAnalyzer

        Returns:
            A modified structure that is oxidation state decorated.
        """
        from pymatgen.analysis.bond_valence import BVAnalyzer
        new = BVAnalyzer(**kwargs).get_oxi_state_decorated_structure(self)
        return self.__class__.as_structure(new)

    @property
    def reciprocal_lattice(self):
        """
        Reciprocal lattice of the structure. Note that this is the standard
        reciprocal lattice used for solid state physics with a factor of 2 * pi
        i.e.  a_j . b_j = 2pi delta_ij

        If you are looking for the crystallographic reciprocal lattice,
        use the reciprocal_lattice_crystallographic property.
        """
        return self._lattice.reciprocal_lattice

    def spget_lattice_type(self, symprec=1e-3, angle_tolerance=5) -> str:
        """
        Call spglib to get the lattice for the structure, e.g., (triclinic,
        orthorhombic, cubic, etc.). This is the same than the
        crystal system with the exception of the hexagonal/rhombohedral lattice

        Args:
            symprec (float): Symmetry precision for distance
            angle_tolerance (float): Tolerance on angles.

        Returns:
            (str): Lattice type for structure or None if type cannot be detected.
        """
        spgan = SpacegroupAnalyzer(self, symprec=symprec, angle_tolerance=angle_tolerance)
        return spgan.get_lattice_type()

    def spget_equivalent_atoms(self, symprec=1e-3, angle_tolerance=5, printout=False):
        """
        Call spglib_ to find the inequivalent atoms and build symmetry tables.

        Args:
            symprec (float): Symmetry precision for distance.
            angle_tolerance (float): Tolerance on angles.
            printout (bool): True to print symmetry tables.

        Returns:
            ``namedtuple`` (irred_pos, eqmap, spgdata) with the following attributes::

                * irred_pos: array giving the position of the i-th irred atom in the structure.
                    The number of irred atoms is len(irred_pos).
                *   eqmap: Mapping irred atom position --> list with positions of symmetrical atoms.
                *   wyckoffs: Wyckoff letters.
                *   wyck_mult: Array with Wyckoff multiplicity.
                *   wyck_labels: List of labels with Wyckoff multiplicity and letter e.g. 3a
                *   site_labels: Labels for each site in computed from element symbol and wyckoff positions e.g Si2a
                *   spgdata: spglib dataset with additional data reported by spglib_.

         :Example:

            for irr_pos in irred_pos:
                eqmap[irr_pos]   # List of symmetrical positions associated to the irr_pos atom.
        """
        natom = len(self)
        spgan = SpacegroupAnalyzer(self, symprec=symprec, angle_tolerance=angle_tolerance)
        spgdata = spgan.get_symmetry_dataset()
        equivalent_atoms = spgdata["equivalent_atoms"]
        wyckoffs = np.array(spgdata["wyckoffs"])

        wyck_mult = [np.count_nonzero(equivalent_atoms == equivalent_atoms[i]) for i in range(natom)]
        wyck_mult = np.array(wyck_mult, dtype=int)

        irred_pos = []
        eqmap = collections.defaultdict(list)
        for pos, eqpos in enumerate(equivalent_atoms):
            eqmap[eqpos].append(pos)
            # Add it to irred_pos if it's irreducible.
            if pos == eqpos: irred_pos.append(pos)

        # Convert to numpy arrays
        irred_pos = np.array(irred_pos)
        for eqpos in eqmap:
            eqmap[eqpos] = np.array(eqmap[eqpos], dtype=int)

        if printout:
            print("Found %d inequivalent position(s):" % len(irred_pos))
            for i, irr_pos in enumerate(sorted(eqmap.keys())):
                print("Wyckoff position: (%s%s)" % (wyck_mult[irr_pos], wyckoffs[irr_pos]))
                print("\t[%d]: %s" % (irr_pos, repr(self[irr_pos])))
                for eqind in eqmap[irr_pos]:
                    if eqind == irr_pos: continue
                    print("\t[%d]: %s" % (eqind, repr(self[eqind])))
            print("")

        # Build list of labels from multiplicity and name: e.g. 3a
        wyck_labels = np.array(["%s%s" % (wmul, wsymb) for wsymb, wmul in zip(wyckoffs, wyck_mult)])

        # Build labels for sites with chemical element.
        site_labels = []
        for i, (site, wsymb, wmul) in enumerate(zip(self, wyckoffs, wyck_mult)):
            site_labels.append("%s%d (%s%s)" % (site.specie.symbol, i, wmul, wsymb))

        return dict2namedtuple(irred_pos=irred_pos, eqmap=eqmap, wyckoffs=wyckoffs,
                               wyck_mult=wyck_mult, wyck_labels=wyck_labels,
                               site_labels=np.array(site_labels), spgdata=spgdata)

    def spget_summary(self, symprec=1e-3, angle_tolerance=5, site_symmetry=False, verbose=0) -> str:
        """
        Return string with full information about crystalline structure i.e.
        space group, point group, wyckoff positions, equivalent sites.

        Args:
            symprec (float): Symmetry precision for distance.
            angle_tolerance (float): Tolerance on angles.
            site_symmetry: True to show site symmetries i.e. the point group operations that leave the site invariant.
            verbose (int): Verbosity level.
        """
        spgan = SpacegroupAnalyzer(self, symprec=symprec, angle_tolerance=angle_tolerance)
        spgdata = spgan.get_symmetry_dataset()
        # Get spacegroup number computed by Abinit if available.
        abispg_number = None if self.abi_spacegroup is None else self.abi_spacegroup.spgid

        # Print lattice info
        outs = ["Full Formula ({s})".format(s=self.composition.formula),
                "Reduced Formula: {}".format(self.composition.reduced_formula)]
        app = outs.append
        to_s = lambda x: "%0.6f" % x
        outs.append("abc   : " + " ".join([to_s(i).rjust(10) for i in self.lattice.abc]))
        outs.append("angles: " + " ".join([to_s(i).rjust(10) for i in self.lattice.angles]))
        app("")
        app("Spglib space group info (magnetic symmetries not taken into account).")
        app("Spacegroup: %s (%s), Hall: %s, Abinit spg_number: %s" % (
             spgan.get_space_group_symbol(), spgan.get_space_group_number(), spgan.get_hall(), str(abispg_number)))
        app("Crystal_system: %s, Lattice_type: %s, Point_group: %s" % (
            spgan.get_crystal_system(), spgan.get_lattice_type(), spgan.get_point_group_symbol()))
        app("")

        wickoffs, equivalent_atoms = spgdata["wyckoffs"], spgdata["equivalent_atoms"]
        header = ["Idx", "Symbol", "Reduced_Coords", "Wyckoff", "EqIdx"]

        if site_symmetry:
            header.append("site_symmetry")
            sitesym_labels = self.spget_site_symmetries()

        table = [header]
        for i, site in enumerate(self):
            mult = np.count_nonzero(equivalent_atoms == equivalent_atoms[i])
            row = [
                i,
                site.species_string,
                "%+.5f %+.5f %+.5f" % tuple(site.frac_coords),
                "(%s%s)" % (mult, wickoffs[i]),
                "%d" % equivalent_atoms[i],
            ]
            if site_symmetry: row.append(sitesym_labels[i])

            table.append(row)

        from tabulate import tabulate
        app(tabulate(table, headers="firstrow"))

        # Print entire dataset.
        if verbose > 1:
            app("\nSpglib dataset:")
            app(pformat(spgdata, indent=4))

        return "\n".join(outs)

    @property
    def abi_spacegroup(self):
        """
        :class:`AbinitSpaceGroup` instance with Abinit symmetries read from the netcd file.
        None if abinit symmetries are not available e.g. if the structure has been created
        from a CIF file.
        """
        try:
            return self._abi_spacegroup
        except AttributeError:
            return None

    def set_abi_spacegroup(self, spacegroup) -> None:
        """``AbinitSpaceGroup`` setter."""
        self._abi_spacegroup = spacegroup

    @property
    def has_abi_spacegroup(self) -> bool:
        """True is the structure contains info on the spacegroup."""
        return self.abi_spacegroup is not None

    def spgset_abi_spacegroup(self, has_timerev, overwrite=False):
        """
        Call spglib to find the spacegroup of the crystal, create new
        :class:`AbinitSpaceGroup` object and store it in ``self.abi_spacegroup``.

        Args:
            has_timerev (bool): True if time-reversal can be used.
            overwrite (bool): By default, the method raises `ValueError` if the object
                already has the list of symmetries found by Abinit.

        Returns: :class:`AbinitSpaceGroup`

        .. warning:

            This method should be called only if the Abipy structure does not have
            spacegroup symmetries e.g. if we are reading a CIF file or if the structure
            is initialized from an output file produced by another code.
        """
        if self.has_abi_spacegroup and not overwrite:
            raise ValueError(("Structure object already has an Abinit spacegroup object.\n"
                              "Use `overwrite=True` to allow modification."))

        msg = ("Structure object does not have symmetry operations computed from Abinit.\n"
               "Calling spglib to get symmetry operations.")
        cprint(msg, "magenta")

        spglib_data = SpacegroupAnalyzer(self).get_symmetry_dataset()
        spgid = spglib_data["number"]
        symrel, tnons = spglib_data["rotations"], spglib_data["translations"]
        # TODO: Anti-ferromagnetic symmetries are not supported by spglib
        symafm = [1] * len(symrel)

        abispg = AbinitSpaceGroup(spgid, symrel, tnons, symafm, has_timerev, inord="C")
        self.set_abi_spacegroup(abispg)

        return abispg

    @property
    def indsym(self):
        """
        Compute indsym (natom, nsym, 4) array.

        For each isym, iatom, the fourth element is label of atom into
        which iatom is sent by INVERSE of symmetry operation isym;
        first three elements are the primitive translations which must be
        subtracted after the transformation to get back to the original unit cell (see symatm.F90).
        """
        if getattr(self, "_indsym", None) is not None: return self._indsym
        if not self.has_abi_spacegroup:
            self.spgset_abi_spacegroup(has_timerev=True, overwrite=False)

        from abipy.core.symmetries import indsym_from_symrel
        self._indsym = indsym_from_symrel(self.abi_spacegroup.symrel, self.abi_spacegroup.tnons, self, tolsym=1e-8)
        return self._indsym

    @indsym.setter
    def indsym(self, indsym):
        """Set indsym array."""
        if getattr(self, "_indsym", None) is not None:
            cprint("structure.indsym is already set!", "yellow")
        self._indsym = indsym

    @lazy_property
    def site_symmetries(self):
        """Object with SiteSymmetries."""
        from abipy.core.site_symmetries import SiteSymmetries
        return SiteSymmetries(self)

    # TODO: site_symmetry or spget_site_symmetries?
    def spget_site_symmetries(self):
        import spglib
        indsym = self.indsym
        symrel, symafm = self.abi_spacegroup.symrel, self.abi_spacegroup.symafm
        nsym = len(symrel)
        sitesym_labels = []
        for iatom, site in enumerate(self):
            rotations = [symrel[isym] for isym in range(nsym) if
                         indsym[iatom, isym, 3] == iatom and symafm[isym] == +1]
            # Passing a 0-length rotations list to spglib can segfault.
            herm_symbol, ptg_num = "1", 1
            if len(rotations) != 0:
                herm_symbol, ptg_num, trans_mat = spglib.get_pointgroup(rotations)

            sitesym_labels.append("%s (#%d,nsym:%d)" % (herm_symbol.strip(), ptg_num, len(rotations)))

        return sitesym_labels

    def abiget_spginfo(self, tolsym=None, pre=None) -> dict:
        """
        Call Abinit to get spacegroup information.
        Return dictionary with e.g.
        {'bravais': 'Bravais cF (face-center cubic)', 'spg_number': 227, 'spg_symbol': 'Fd-3m'}.

        Args:
            tolsym: Abinit tolsym input variable. None correspondes to the default value.
            pre: Keywords in dictionary are prepended with this string
        """
        from abipy.data.hgh_pseudos import HGH_TABLE
        from abipy.abio import factories
        gsinp = factories.gs_input(self, HGH_TABLE, spin_mode="unpolarized")
        gsinp["chkprim"] = 0
        d = gsinp.abiget_spacegroup(tolsym=tolsym, retdict=True)
        if pre: d = {pre + k: v for k, v in d.items()}
        return d

    def print_neighbors(self, radius=2.0) -> None:
        """
        Get neighbors for each atom in the unit cell, out to a distance ``radius`` in Angstrom
        Print results.
        """
        print(" ")
        print("Finding neighbors for each atom in the unit cell, out to a distance %s (Angstrom)" % radius)
        print(" ")

        ns = self.get_all_neighbors_old(radius, include_index=False)
        for i, (site, sited_list) in enumerate(zip(self, ns)):
            print("[%s] site %s has %s neighbors:" % (i, repr(site), len(sited_list)))
            for s, dist in sorted(sited_list, key=lambda t: t[1]):
                print("\t", repr(s), " at distance", dist)
            print("")

    @lazy_property
    def has_zero_dynamical_quadrupoles(self):
        """
        Dynamical quadrupoles are nonzero in all noncentrosymmetric crystals,
        but also in centrosymmetric ones if one or more atoms are placed at noncentrosymmetric sites.
        """
        def create_image(s1, s2):
            """
            Creates the image of s2 through s1
            This image is a fictitious atom in the structure
            """
            image = PeriodicSite.from_dict(s2.as_dict())
            image.coords = s1.coords - (s2.coords - s1.coords)
            image.frac_coords = s1.frac_coords - (s2.frac_coords - s1.frac_coords)

            return image

        def check_image(structure, site):
            """
            Checks if a fictitious site is an image of a site of the structure
            """
            for site in structure.sites:
                if site.is_periodic_image(site):
                    return True

            return False

        # If the centrosymmetry is broken at a given atomic site of the given structure,
        # returns False. Else, return True
        sites = self.sites

        for s1 in sites:
            for s2 in sites:
                # Do not take s1 = s2 into account
                if s2 != s1:
                    # Create the image of s2 through s1 (fictitious atom)
                    image = create_image(s1, s2)
                    is_image = check_image(self, image)
                    if not is_image:
                        return False

        return True


    @lazy_property
    def hsym_kpath(self):
        """
        Returns an instance of :class:`pymatgen.symmetry.bandstructure.HighSymmKpath`.
        (Database of high symmetry k-points and high symmetry lines).
        """
        from pymatgen.symmetry.bandstructure import HighSymmKpath
        return HighSymmKpath(self)

    @lazy_property
    def hsym_kpoints(self):
        """|KpointList| object with the high-symmetry K-points."""
        # Get mapping name --> frac_coords for the special k-points in the database.
        name2frac_coords = self.hsym_kpath.kpath["kpoints"]
        kpath = self.hsym_kpath.kpath["path"]

        frac_coords, names = [], []
        for segment in kpath:
            for name in segment:
                fc = name2frac_coords[name]
                frac_coords.append(fc)
                names.append(name)

        # Build KpointList instance.
        from .kpoints import KpointList
        return KpointList(self.reciprocal_lattice, frac_coords, weights=None, names=names)

    def get_kcoords_from_names(self, knames, cart_coords=False) -> np.ndarray:
        """
        Return numpy array with the fractional coordinates of the high-symmetry k-points listed in `knames`.

        Args:
            knames: List of strings with the k-point labels.
            cart_coords: True if the ``coords`` dataframe should contain Cartesian cordinates
                instead of Reduced coordinates.
        """
        kname2frac = {k.name: k.frac_coords for k in self.hsym_kpoints}

        # Add aliases for Gamma.
        if r"$\Gamma$" in kname2frac:
            kname2frac["G"] = kname2frac[r"$\Gamma$"]
            kname2frac["Gamma"] = kname2frac[r"$\Gamma$"]

        try:
            kcoords = np.reshape([kname2frac[name] for name in list_strings(knames)], (-1, 3))
        except KeyError:
            cprint("Internal list of high-symmetry k-points:\n%s" % str(self.hsym_kpoints))
            raise

        if cart_coords:
            kcoords = self.reciprocal_lattice.get_cartesian_coords(kcoords)

        return kcoords

    @lazy_property
    def hsym_stars(self) -> list:
        """
        List of |KpointStar| objects. Each star is associated to one of the special k-points
        present in the pymatgen database.
        """
        # Construct the stars.
        return [kpoint.compute_star(self.abi_spacegroup.fm_symmops) for kpoint in self.hsym_kpoints]

    # TODO
    #def get_star_kpoint(self, kpoint):

    #    # Call spglib to get spacegroup if Abinit spacegroup is not available.
    #    if self.abi_spacegroup is None:
    #        self.spgset_abi_spacegroup(has_timerev=not options.no_time_reversal)

    #    kpoint = Kpoint(options.kpoint, self.reciprocal_lattice)
    #    kstar = kpoint.compute_star(self.abi_spacegroup, wrap_tows=True)
    #    return kstar
    #    #print("Found %s points in the star of %s\n" % (len(kstar), repr(kpoint)))
    #    #for k in kstar:
    #    #    print(4 * " ", repr(k))

    def get_sorted_structure_z(self) -> Structure:
        """Order the structure according to increasing Z of the elements"""
        return self.__class__.from_sites(sorted(self.sites, key=lambda site: site.specie.Z))

    def findname_in_hsym_stars(self, kpoint):
        """
        Returns the name of the special k-point, None if kpoint is unknown.
        """
        if self.abi_spacegroup is None: return None

        from .kpoints import Kpoint
        kpoint = Kpoint.as_kpoint(kpoint, self.reciprocal_lattice)

        # Try to find kpoint in hsym_stars without taking into accout symmetry operation (compare with base_point)
        # Important if there are symmetry equivalent k-points in hsym_kpoints e.g. K and U in FCC lattice
        # as U should not be mapped onto K as done in the second loop below.
        from .kpoints import issamek
        for star in self.hsym_stars:
            if issamek(kpoint.frac_coords, star.base_point.frac_coords):
                return star.name

        # Now check if kpoint is in one of the stars.
        for star in self.hsym_stars:
            i = star.find(kpoint)
            if i != -1:
                #print("input kpt:", kpoint, "star image", star[i], star[i].name)
                return star.name
        else:
            return None

    def get_symbol2indices(self) -> dict:
        """
        Return a dictionary mapping chemical symbols to numpy array with the position of the atoms.

        Example:

            MgB2 --> {Mg: [0], B: [1, 2]}
        """
        return {symbol: np.array(self.indices_from_symbol(symbol)) for symbol in self.symbol_set}

    def get_symbol2coords(self) -> dict:
        """
        Return a dictionary mapping chemical symbols to a [ntype_symbol, 3] numpy array
        with the fractional coordinates.
        """
        # TODO:
        #use structure.frac_coords but add reshape in pymatgen.
        #fcoords = np.reshape([s.frac_coords for s in self], (-1, 3))
        coords = {}
        for symbol in self.symbol_set:
            coords[symbol] = np.reshape(
                [site.frac_coords for site in self if site.specie.symbol == symbol], (-1, 3))

        return coords

    def dot(self, coords_a, coords_b, space="r", frac_coords=False):
        """
        Compute the scalar product of vector(s) either in real space or
        reciprocal space.

        Args:
            coords (3x1 array): Array-like object with the coordinates.
            space (str): "r" for real space, "g" for reciprocal space.
            frac_coords (bool): Whether the vector corresponds to fractional or
                cartesian coordinates.

        Returns:
            one-dimensional `numpy` array.
        """
        lattice = {"r": self.lattice,
                   "g": self.reciprocal_lattice}[space.lower()]
        return lattice.dot(coords_a, coords_b, frac_coords=frac_coords)

    def norm(self, coords, space="r", frac_coords=True):
        """
        Compute the norm of vector(s) either in real space or reciprocal space.

        Args:
            coords (3x1 array): Array-like object with the coordinates.
            space (str): "r" for real space, "g" for reciprocal space.
            frac_coords (bool): Whether the vector corresponds to fractional or
                cartesian coordinates.

        Returns:
            one-dimensional `numpy` array.
        """
        return np.sqrt(self.dot(coords, coords, space=space, frac_coords=frac_coords))

    def scale_lattice(self, new_volume) -> Structure:
        """
        Return a new |Structure| with volume new_volume by performing a
        scaling of the lattice vectors so that length proportions and angles are preserved.
        """
        new_lattice = self.lattice.scale(new_volume)
        return self.__class__(new_lattice, self.species, self.frac_coords)

    def get_dict4pandas(self, symprec=1e-2, angle_tolerance=5.0, with_spglib=True) -> dict:
        """
        Return a dict with the most important structural parameters:

            - Chemical formula and number of atoms.
            - Lattice lengths, angles and volume.
            - The spacegroup number computed by Abinit (set to None if not available).
            - The spacegroup number and symbol computed by spglib (if `with_spglib`).

        Useful to construct pandas DataFrames

        Args:
            with_spglib (bool): If True, spglib is invoked to get the spacegroup symbol and number
            symprec (float): Symmetry precision used to refine the structure.
            angle_tolerance (float): Tolerance on angles.
        """
        abc, angles = self.lattice.abc, self.lattice.angles

        # Get spacegroup info from spglib.
        spglib_symbol, spglib_number, spglib_lattice_type = None, None, None
        if with_spglib:
            try:
                spglib_symbol, spglib_number = self.get_space_group_info(symprec=symprec,
                                                                         angle_tolerance=angle_tolerance)
                spglib_lattice_type = self.spget_lattice_type(symprec=symprec, angle_tolerance=angle_tolerance)
            except Exception as exc:
                cprint("Spglib couldn't find space group symbol and number for composition: `%s`" %
                        str(self.composition), "red")
                print("Exception:\n", exc)

        # Get spacegroup number computed by Abinit if available.
        abispg_number = None if self.abi_spacegroup is None else self.abi_spacegroup.spgid

        od = OrderedDict([
            ("formula", self.formula), ("natom", self.num_sites),
            ("alpha", angles[0]), ("beta", angles[1]), ("gamma", angles[2]),
            ("a", abc[0]), ("b", abc[1]), ("c", abc[2]), ("volume", self.volume),
            ("abispg_num", abispg_number),
        ])
        if with_spglib:
            od["spglib_symb"] = spglib_symbol
            od["spglib_num"] = spglib_number
            od["spglib_lattice_type"] = spglib_lattice_type

        return od

    def get_symb2coords_dataframe(self, with_cart_coords=False) -> dict:
        """
        Return dictionary mapping element symbol to DataFrame with atomic positions
        in cartesian coordinates.

        Args:
            with_cart_coords: True if Cartesian coordinates should be added as well.
        """
        if with_cart_coords:
            group = {symb: {"site_idx": [], "frac_coords": [], "cart_coords": []} for symb in self.symbol_set}
        else:
            group = {symb: {"site_idx": [], "frac_coords": []} for symb in self.symbol_set}

        for idx, site in enumerate(self):
            symb = site.specie.symbol
            group[symb]["site_idx"].append(idx)
            group[symb]["frac_coords"].append(site.frac_coords)
            if with_cart_coords:
                group[symb]["cart_coords"].append(site.coords)

        out = {symb: pd.DataFrame.from_dict(d) for symb, d in group.items()}
        # Use site_idx and new index.
        for df in out.values():
            df.set_index("site_idx", inplace=True)

        return out

    @add_fig_kwargs
    def plot(self, **kwargs):
        """
        Plot structure in 3D with matplotlib. Return matplotlib Figure.
        See plot_structure for kwargs.
        """
        from abipy.tools.plotting import plot_structure
        return plot_structure(self, **kwargs)

    @add_plotly_fig_kwargs
    def plotly(self, **kwargs):
        """
        Plot structure in 3D with plotly. Return plotly Figure.
        See plot_structure for kwargs
        """
        from abipy.tools.plotting import plotly_structure
        return plotly_structure(self, **kwargs)

    @add_fig_kwargs
    def plot_bz(self, ax=None, pmg_path=True, with_labels=True, **kwargs):
        """
        Use matplotlib to plot the symmetry line path in the Brillouin Zone.

        Args:
            ax: matplotlib :class:`Axes` or None if a new figure should be created.
            pmg_path (bool): True if the default path used in pymatgen should be show.
            with_labels (bool): True to plot k-point labels.

        Returns: |matplotlib-Figure|.
        """
        from pymatgen.electronic_structure.plotter import plot_brillouin_zone, plot_brillouin_zone_from_kpath
        labels = None if not with_labels else self.hsym_kpath.kpath["kpoints"]
        if pmg_path:
            return plot_brillouin_zone_from_kpath(self.hsym_kpath, ax=ax, show=False, **kwargs)
        else:
            return plot_brillouin_zone(self.reciprocal_lattice, ax=ax, labels=labels, show=False, **kwargs)

    @add_plotly_fig_kwargs
    def plotly_bz(self, fig=None, pmg_path=True, with_labels=True, **kwargs):
        """
        Use plotly to plot the symmetry line path in the Brillouin Zone.

        Args:
            fig: plotly figure or None if a new figure should be created.
            pmg_path (bool): True if the default path used in pymatgen should be show.
            with_labels (bool): True to plot k-point labels.

        Returns: plotly.graph_objects.Figure
        """
        from abipy.tools.plotting import plotly_brillouin_zone_from_kpath, plotly_brillouin_zone
        labels = None if not with_labels else self.hsym_kpath.kpath["kpoints"]
        if pmg_path:
            return plotly_brillouin_zone_from_kpath(self.hsym_kpath, fig=fig, show=False, **kwargs)
        else:
            return plotly_brillouin_zone(self.reciprocal_lattice, fig=fig, labels=labels, show=False, **kwargs)

    @add_fig_kwargs
    def plot_xrd(self, wavelength="CuKa", symprec=0, debye_waller_factors=None,
                 two_theta_range=(0, 90), annotate_peaks=True, ax=None, **kwargs) -> Figure:
        """
        Use pymatgen :class:`XRDCalculator` to show the XRD plot.

        Args:
            wavelength (str/float): The wavelength can be specified as either a
                float or a string. If it is a string, it must be one of the
                supported definitions in the AVAILABLE_RADIATION class
                variable, which provides useful commonly used wavelengths.
                If it is a float, it is interpreted as a wavelength in
                angstroms. Defaults to "CuKa", i.e, Cu K_alpha radiation.
            symprec (float): Symmetry precision for structure refinement. If
                set to 0, no refinement is done. Otherwise, refinement is
                performed using spglib_ with provided precision.
            debye_waller_factors ({element symbol: float}): Allows the
                specification of Debye-Waller factors. Note that these
                factors are temperature dependent.
            two_theta_range ([float of length 2]): Tuple for range of
                two_thetas to calculate in degrees. Defaults to (0, 90). Set to
                None if you want all diffracted beams within the limiting
                sphere of radius 2 / wavelength.
            annotate_peaks (bool): Whether to annotate the peaks with plane information.
            ax: matplotlib :class:`Axes` or None if a new figure should be created.

        Returns: |matplotlib-Figure|
        """
        ax, fig, plt = get_ax_fig_plt(ax=ax)
        from pymatgen.analysis.diffraction.xrd import XRDCalculator
        xrd = XRDCalculator(wavelength=wavelength, symprec=symprec, debye_waller_factors=debye_waller_factors)
        xrd.get_plot(self, two_theta_range=two_theta_range, annotate_peaks=annotate_peaks, ax=ax)

        return fig

    def yield_figs(self, **kwargs):  # pragma: no cover
        """
        This function *generates* a predefined list of matplotlib figures with minimal input from the user.
        """
        yield self.plot(show=False)
        yield self.plot_bz(show=False)

    def export(self, filename, visu=None, verbose=1):
        """
        Export the crystalline structure to file ``filename``.

        Args:
            filename (str): String specifying the file path and the file format.
                The format is defined by the file extension. filename="prefix.xsf", for example,
                will produce a file in XSF format. An *empty* prefix, e.g. ".xsf" makes the code use a temporary file.
            visu: |Visualizer| subclass. By default, this method returns the first available
                visualizer that supports the given file format. If visu is not None, an
                instance of visu is returned. See |Visualizer| for the list of applications and formats supported.
            verbose: Verbosity level

        Returns: ``Visulizer`` instance.
        """
        if "." not in filename:
            raise ValueError("Cannot detect extension in filename %s:" % filename)

        tokens = filename.strip().split(".")
        ext = tokens[-1]
        #print("tokens", tokens, "ext", ext)
        #if ext == "POSCAR":

        if not tokens[0]:
            # filename == ".ext" ==> Create temporary file.
            # nbworkdir in cwd is needed when we invoke the method from a notebook.
            from abipy.core.globals import abinb_mkstemp
            _, rpath = abinb_mkstemp(force_abinb_workdir=False, use_relpath=False,
                                     suffix="." + ext, text=True)
            #if abilab.in_notebook():
            #    _, filename = tempfile.mkstemp(suffix="." + ext, dir=abilab.get_abipy_nbworkdir(), text=True)
            #else:
            #    _, filename = tempfile.mkstemp(suffix="." + ext, text=True)

        if ext.lower() in ("xsf", "poscar", "cif"):
            if verbose:
                print("Writing data to:", filename, "with fmt:", ext.lower())
            s = self.to(fmt=ext)
            with open(filename, "wt") as fh:
                fh.write(s)

        if visu is None:
            return Visualizer.from_file(filename)
        else:
            return visu(filename)

    def get_chemview(self, **kwargs): # pragma: no cover
        """
        Visualize structure inside the jupyter notebook using chemview package.
        """
        from pymatgen.vis.structure_chemview import quick_view
        return quick_view(self, **kwargs)

    def plot_vtk(self, show=True, **kwargs):
        """
        Visualize structure with VTK. Requires vVTK python bindings.

        Args:
            show: True to show structure immediately.
            kwargs: keyword arguments passed to :class:`StructureVis`.

        Return: StructureVis object.
        """
        from pymatgen.vis.structure_vtk import StructureVis
        vis = StructureVis(**kwargs)
        vis.set_structure(self, to_unit_cell=True)
        if show: vis.show()
        return vis

    def plot_mayaview(self, figure=None, show=True, **kwargs):
        """Visualize structure with mayavi."""
        from abipy.display import mvtk
        return mvtk.plot_structure(self, figure=figure, show=show, **kwargs)

    @add_fig_kwargs
    def plot_atoms(self, rotations="default", **kwargs):
        """
        Plot 2d representation with matplotlib using ASE `plot_atoms` function.

        Args:
            rotations: String or List of strings.
                Each string defines a rotation (in degrees) in the form '10x,20y,30z'
                Note that the order of rotation matters, i.e. '50x,40z' is different from '40z,50x'.
            kwargs: extra kwargs passed to plot_atoms ASE function.

        Returns: |matplotlib-Figure|
        """
        if rotations == "default":
            rotations = [
                "", "90x", "90y",
                "45x,45y", "45y,45z", "45x,45z",
            ]
        else:
            rotations = list_strings(rotations)

        nrows, ncols, num_plots = 1, 1, len(rotations)
        if num_plots > 1:
            ncols = 3
            nrows = num_plots // ncols + num_plots % ncols

        ax_mat, fig, plt = get_axarray_fig_plt(None, nrows=nrows, ncols=ncols,
                                                sharex=False, sharey=True, squeeze=False)

        # don't show the last ax if num_plots is odd.
        if num_plots % ncols != 0: ax_mat[-1, -1].axis("off")

        from ase.visualize.plot import plot_atoms
        atoms = self.to_ase_atoms()
        for rotation, ax in zip(rotations, ax_mat.flat):
            plot_atoms(atoms, ax=ax, rotation=rotation, **kwargs)
            ax.set_axis_off()
            if rotation:
                ax.set_title("rotation: %s" % str(rotation), fontsize=6)

        return fig

    def get_ngl_view(self): # pragma: no cover
        """
        Visualize the structure with nglview inside the jupyter notebook.
        """
        try:
            import nglview as nv
        except ImportError:
            raise ImportError("nglview is not installed. See https://github.com/arose/nglview")

        view = nv.show_pymatgen(self)
        view.add_unitcell()
        return view

    def get_crystaltk_view(self): # pragma: no cover
        """
        Visualize the structure with crystal_toolkit inside the jupyter notebook.
        """
        try:
            # FIXME: It seems they changed the API.
            from crystal_toolkit import view
        except ImportError:
            raise ImportError("crystal_toolkit is not installed. See https://docs.crystaltoolkit.org/jupyter")

        return view(self)

    def get_jsmol_view(self, symprec=None, verbose=0, **kwargs): # pragma: no cover
        """
        Visualize the structure with jsmol inside the jupyter notebook.

        Args:
            symprec (float): If not none, finds the symmetry of the structure
                and writes the CIF with symmetry information.
                Passes symprec to the spglib SpacegroupAnalyzer.
            verbose: Verbosity level.
        """
        try:
            from jupyter_jsmol import JsmolView
        except ImportError:
            raise ImportError("jupyter_jsmol is not installed. See https://github.com/fekad/jupyter-jsmol")

        cif_str = self.write_cif_with_spglib_symms(None, symprec=symprec, ret_string=True)
        #print("cif_str:\n", cif_str)
        #return JsmolView.from_str(cif_str)

        #from IPython.display import display, HTML
        # FIXME TEMPORARY HACK TO LOAD JSMOL.js
        # See discussion at
        #   https://stackoverflow.com/questions/16852885/ipython-adding-javascript-scripts-to-ipython-notebook
        #display(HTML('<script type="text/javascript" src="/nbextensions/jupyter-jsmol/jsmol/JSmol.min.js"></script>'))

        jsmol = JsmolView(color='white')
        #display(jsmol)
        cmd = 'load inline "%s" {1 1 1}' % cif_str
        if verbose: print("executing cmd:", cmd)
        jsmol.script(cmd)

        return jsmol

    def visualize(self, appname="vesta"):
        """
        Visualize the crystalline structure with visualizer.
        See |Visualizer| for the list of applications and formats supported.
        """
        if appname in ("mpl", "matplotlib"): return self.plot()
        if appname == "vtk": return self.plot_vtk()
        if appname == "mayavi": return self.plot_mayaview()

        # Get the Visualizer subclass from the string.
        visu = Visualizer.from_name(appname)

        # Try to export data to one of the formats supported by the visualizer
        # Use a temporary file (note "." + ext)
        for ext in visu.supported_extensions():
            ext = "." + ext
            try:
                return self.export(ext, visu=visu)()
            except visu.Error as exc:
                cprint(str(exc), color="red")
                pass
        else:
            raise visu.Error("Don't know how to export data for %s" % appname)

    def convert(self, fmt: str = "cif", **kwargs) -> str:
        """
        Return string with the structure in the given format `fmt`
        Options include: "abivars", "cif", "xsf", "poscar", "siesta", "wannier90", "cssr", "json".
        """
        if fmt in ("abivars", "abinit"):
            return self.abi_string
        elif fmt == "abipython":
            return pformat(self.to_abivars(), indent=4)
        elif fmt == "qe":
            from pymatgen.io.pwscf import PWInput
            return str(PWInput(self, pseudo={s: s + ".pseudo" for s in self.symbol_set}))
        elif fmt == "siesta":
            return structure2siesta(self)
        elif fmt in ("wannier90", "w90"):
            from abipy.wannier90.win import structure2wannier90
            return structure2wannier90(self)
        elif fmt.lower() == "poscar":
            # Don't call super for poscar because we need more significant_figures to
            # avoid problems with abinit space group routines where the default numerical tolerance is tight.
            from pymatgen.io.vasp import Poscar
            try:
                return Poscar(self).get_str(significant_figures=12)
            except AttributeError:
                return Poscar(self).get_string(significant_figures=12)

        elif fmt.lower() == "lammps":
            from pymatgen.io.lammps.data import LammpsData
            # Convert the structure to a LAMMPS data file
            lammps_data = LammpsData.from_structure(self)
            return lammps_data.get_str()

        else:
            return super().to(fmt=fmt, **kwargs)

    def displace(self, displ, eta, frac_coords=True, normalize=True):
        """
        Displace the sites of the structure along the displacement vector displ.

        The displacement vector is first rescaled so that the maxium atomic displacement
        is one Angstrom, and then multiplied by eta. Hence passing eta=0.001, will move
        all the atoms so that the maximum atomic displacement is 0.001 Angstrom.

        Args:
            displ: Displacement vector with 3*len(self) entries (fractional coordinates).
            eta: Scaling factor.
            frac_coords: Boolean stating whether the vector corresponds to fractional or cartesian coordinates.
        """
        # Get a copy since we are going to modify displ.
        displ = np.reshape(displ, (-1, 3)).copy()

        if len(displ) != len(self):
            raise ValueError("Displ must contains 3 * natom entries")
        if np.iscomplexobj(displ):
            raise TypeError("Displacement cannot be complex")

        if not frac_coords:
            # Convert to fractional coordinates.
            displ = np.reshape([self.lattice.get_fractional_coords(vec) for vec in displ], (-1,3))

        # Normalize the displacement so that the maximum atomic displacement is 1 Angstrom.
        if normalize:
            dnorm = self.norm(displ, space="r")
            displ /= np.max(np.abs(dnorm))

        # Displace the sites.
        for i in range(len(self)):
            self.translate_sites(indices=i, vector=eta * displ[i, :], frac_coords=True)

    def get_smallest_supercell(self, qpoint, max_supercell):
        """
        Args:
            qpoint: q vector in reduced coordinates in reciprocal space.
            max_supercell: vector with the maximum supercell size

        Returns: the scaling matrix of the supercell
        """
        if np.allclose(qpoint, 0.0):
            return np.eye(3, 3)

        l = max_supercell

        # Inspired from Exciting Fortran code phcell.F90
        # It should be possible to improve this coding.
        scale_matrix = np.zeros((3, 3), dtype=int)
        dmin = np.inf
        found = False

        # Try to reduce the matrix
        rprimd = self.lattice.matrix
        for l1 in np.arange(-l[0], l[0] + 1):
            for l2 in np.arange(-l[1], l[1] + 1):
                for l3 in np.arange(-l[2], l[2] + 1):
                    lnew = np.array([l1, l2, l3])
                    ql = np.dot(lnew, qpoint)
                    # Check if integer and non zero !
                    if np.abs(ql - np.round(ql)) < 1e-6:
                        Rl = np.dot(lnew, rprimd)
                        # Normalize the displacement so that the maximum atomic displacement is 1 Angstrom.
                        dnorm = np.sqrt(np.dot(Rl, Rl))
                        if dnorm < (dmin-1e-6) and dnorm > 1e-6:
                            found = True
                            scale_matrix[:, 0] = lnew
                            dmin = dnorm
        if not found:
            raise ValueError('max_supercell is not large enough for this q-point')

        found = False
        dmin = np.inf
        for l1 in np.arange(-l[0], l[0] + 1):
            for l2 in np.arange(-l[1], l[1] + 1):
                for l3 in np.arange(-l[2], l[2] + 1):
                    lnew = np.array([l1, l2, l3])
                    # Check if not parallel !
                    cp = np.cross(lnew, scale_matrix[:,0])
                    if np.dot(cp, cp) > 1e-6:
                        ql = np.dot(lnew, qpoint)
                        # Check if integer and non zero !
                        if np.abs(ql - np.round(ql)) < 1e-6:
                            Rl = np.dot(lnew, rprimd)
                            dnorm = np.sqrt(np.dot(Rl, Rl))
                            if dnorm < (dmin-1e-6) and dnorm > 1e-6:
                                found = True
                                scale_matrix[:, 1] = lnew
                                dmin = dnorm
        if not found:
            raise ValueError('max_supercell is not large enough for this q-point')

        dmin = np.inf
        found = False
        for l1 in np.arange(-l[0], l[0] + 1):
            for l2 in np.arange(-l[1], l[1] + 1):
                for l3 in np.arange(-l[2], l[2] + 1):
                    lnew = np.array([l1, l2, l3])
                    # Check if not parallel!
                    cp = np.dot(np.cross(lnew, scale_matrix[:, 0]), scale_matrix[:, 1])
                    if cp > 1e-6:
                        # Should be positive as (R3 X R1).R2 > 0 for abinit!
                        ql = np.dot(lnew, qpoint)
                        # Check if integer and non zero!
                        if np.abs(ql - np.round(ql)) < 1e-6:
                            Rl = np.dot(lnew, rprimd)
                            dnorm = np.sqrt(np.dot(Rl,Rl))
                            if dnorm < (dmin-1e-6) and dnorm > 1e-6:
                                found = True
                                scale_matrix[:, 2] = lnew
                                dmin = dnorm
        if not found:
            raise ValueError('max_supercell is not large enough for this q-point')

        # Fortran 2 python!!!
        return scale_matrix.T.copy()

    def make_doped_supercells(self, scaling_matrix, replaced_atom, dopant_atom):
        """
        Returns a list doped supercell structures, one for each non-equivalent site of the replaced atom.

        Args:
            scaling_matrix: A scaling matrix for transforming the lattice vectors.
                Has to be all integers. Several options are possible:
                a. A full 3x3 scaling matrix defining the linear combination of the old lattice vectors.
                    E.g., [[2,1,0],[0,3,0],[0,0,1]] generates a new structure with lattice vectors
                    a' = 2a + b, b' = 3b, c' = c
                    where a, b, and c are the lattice vectors of the original structure.
                b. A sequence of three scaling factors. e.g., [2, 1, 1]
                   specifies that the supercell should have dimensions 2a x b x c.
                c. A number, which simply scales all lattice vectors by the same factor.
            replaced atom: Symbol of the atom to be replaced (ex: 'Sr')
            dopant_atom: Symbol of the dopant_atom (ex: 'Eu')
        """
        ### list of positions of non-equivalent sites for the replaced atom. ###
        irred = self.spget_equivalent_atoms().eqmap # mapping from inequivalent sites to atoms sites
        positions = self.get_symbol2indices()[replaced_atom] # get indices of the replaced atom

        index_non_eq_sites = []
        for pos in positions:
            if len(irred[pos]) != 0:
                 index_non_eq_sites.append(irred[pos][0])

        doped_supercell = self.copy()
        doped_supercell.make_supercell(scaling_matrix)

        doped_structure_list = []

        for index in index_non_eq_sites:
            final_structure=doped_supercell.copy()
            final_structure.replace(index,dopant_atom)
            doped_structure_list.append(final_structure)

        return doped_structure_list

    def get_trans_vect(self, scale_matrix):
        """
        Returns the translation vectors for a given scale matrix.

        Args:
            scale_matrix: Scale matrix defining the new lattice vectors in term of the old ones

        Return: the translation vectors
        """
        scale_matrix = np.array(scale_matrix, np.int16)
        if scale_matrix.shape != (3, 3):
            scale_matrix = np.array(scale_matrix * np.eye(3), np.int16)

        def range_vec(i):
            low = 0
            high = 0
            for z in scale_matrix[:, i]:
                if z > 0:
                    high += z
                else:
                    low += z
            return np.arange(low, high+1)

        arange = range_vec(0)[:, None] * np.array([1, 0, 0])[None, :]
        brange = range_vec(1)[:, None] * np.array([0, 1, 0])[None, :]
        crange = range_vec(2)[:, None] * np.array([0, 0, 1])[None, :]
        all_points = arange[:, None, None] + brange[None, :, None] + crange[None, None, :]
        all_points = all_points.reshape((-1, 3))

        # find the translation vectors (in terms of the initial lattice vectors)
        # that are inside the unit cell defined by the scale matrix
        # we're using a slightly offset interval from 0 to 1 to avoid numerical precision issues
        #print(scale_matrix)
        inv_matrix = np.linalg.inv(scale_matrix)

        frac_points = np.dot(all_points, inv_matrix)
        tvects = all_points[np.where(np.all(frac_points < 1-1e-10, axis=1)
                                     & np.all(frac_points >= -1e-10, axis=1))]
        assert len(tvects) == np.round(abs(np.linalg.det(scale_matrix)))

        return tvects

    def write_vib_file(self, xyz_file, qpoint, displ, do_real=True, frac_coords=True,
                       scale_matrix=None, max_supercell=None) -> None:
        """
        Write into the file descriptor xyz_file the positions and displacements of the atoms

        Args:
            xyz_file: file_descriptor
            qpoint: qpoint to be analyzed
            displ: eigendisplacements to be analyzed
            do_real: True if you want to get only real part, False means imaginary part
            frac_coords: True if the eigendisplacements are given in fractional coordinates
            scale_matrix: Scale matrix for supercell
            max_supercell: Maximum size of supercell vectors with respect to primitive cell
        """
        if scale_matrix is None:
            if max_supercell is None:
                raise ValueError("If scale_matrix is not provided, please provide max_supercell!")

            scale_matrix = self.get_smallest_supercell(qpoint, max_supercell=max_supercell)

        old_lattice = self._lattice
        new_lattice = Lattice(np.dot(scale_matrix, old_lattice.matrix))

        tvects = self.get_trans_vect(scale_matrix)

        new_displ = np.zeros(3, dtype=float)

        fmtstr = "{{}} {{:.{0}f}} {{:.{0}f}} {{:.{0}f}} {{:.{0}f}} {{:.{0}f}} {{:.{0}f}}\n".format(6)

        for at, site in enumerate(self):
            for t in tvects:
                if do_real:
                    new_displ[:] = np.real(np.exp(2*1j*np.pi*(np.dot(qpoint,t)))*displ[at,:])
                else:
                    new_displ[:] = np.imag(np.exp(2*1j*np.pi*(np.dot(qpoint,t)))*displ[at,:])
                if frac_coords:
                    # Convert to fractional coordinates.
                    new_displ = self.lattice.get_cartesian_coords(new_displ)

                # We don't normalize here !!!
                fcoords = site.frac_coords + t

                coords = old_lattice.get_cartesian_coords(fcoords)

                new_fcoords = new_lattice.get_fractional_coords(coords)

                # New_fcoords -> map into 0 - 1
                new_fcoords = np.mod(new_fcoords, 1)
                coords = new_lattice.get_cartesian_coords(new_fcoords)

                xyz_file.write(fmtstr.format(site.specie, coords[0], coords[1], coords[2],
                               new_displ[0], new_displ[1], new_displ[2]))

    def frozen_2phonon(self, qpoint, displ1, displ2, eta=1, frac_coords=False, scale_matrix=None, max_supercell=None):
        """
        Creates the supercell needed for a given qpoint and adds the displacements.
        The displacements are normalized so that the largest atomic displacement will correspond
        to the value of eta in Angstrom.

        Args:
            qpoint: q vector in reduced coordinate in reciprocal space.
            displ1: first displacement in real space of the atoms.
            displ2: second displacement in real space of the atoms.
            eta: pre-factor multiplying the displacement. Gives the value in Angstrom of the
                largest displacement.
            frac_coords: whether the displacements are given in fractional or cartesian coordinates
            scale_matrix: the scaling matrix of the supercell. If None a scaling matrix suitable for
                the qpoint will be determined.
            max_supercell: mandatory if scale_matrix is None, ignored otherwise. Defines the largest
                supercell in the search for a scaling matrix suitable for the q point.

        Returns:
            A namedtuple with a Structure with the displaced atoms, a numpy array containing the
            displacements applied to each atom and the scale matrix used to generate the supercell.
        """

        if scale_matrix is None:
            if max_supercell is None:
                raise ValueError("scale_matrix is not provided, please provide max_supercell!")

            scale_matrix = self.get_smallest_supercell(qpoint, max_supercell=max_supercell)

        scale_matrix = np.array(scale_matrix, np.int16)
        if scale_matrix.shape != (3, 3):
            scale_matrix = np.array(scale_matrix * np.eye(3), np.int16)

        old_lattice = self._lattice
        new_lattice = Lattice(np.dot(scale_matrix, old_lattice.matrix))

        tvects = self.get_trans_vect(scale_matrix)

        if frac_coords:
            displ1 = np.array((old_lattice.get_cartesian_coords(d) for d in displ1))
            displ2 = np.array((old_lattice.get_cartesian_coords(d) for d in displ2))
        else:
            displ1 = np.array(displ1)
            displ2 = np.array(displ2)

        # from here on displ are in cartesian coordinates
        norm_factor = np.linalg.norm(displ1+displ2, axis=1).max()

        displ1 = eta * displ1 / norm_factor
        displ2 = eta * displ2 / norm_factor

        new_displ1 = np.zeros(3, dtype=float)
        new_displ2 = np.zeros(3, dtype=float)
        new_sites = []
        displ_list = []
        for at,site in enumerate(self):
            for t in tvects:
                new_displ1[:] = np.real(np.exp(2*1j * np.pi * (np.dot(qpoint, t))) * displ1[at,:])
                new_displ2[:] = np.real(np.exp(2*1j * np.pi * (np.dot(qpoint, t))) * displ2[at,:])

                displ_list.append(new_displ1 + new_displ2)
                coords = site.coords + old_lattice.get_cartesian_coords(t) + new_displ1 + new_displ2
                new_site = PeriodicSite(
                    site.species, coords, new_lattice,
                    coords_are_cartesian=True, properties=site.properties,
                    to_unit_cell=True)
                new_sites.append(new_site)

        new_structure = self.__class__.from_sites(new_sites)

        return dict2namedtuple(structure=new_structure, displ=np.array(displ_list), scale_matrix=scale_matrix)

    def frozen_phonon(self, qpoint, displ, eta=1, frac_coords=False, scale_matrix=None, max_supercell=None):
        """
        Creates a supercell with displaced atoms for the specified q-point.
        The displacements are normalized so that the largest atomic displacement will correspond to the
        value of eta in Angstrom.

        Args:
            qpoint: q-vector in reduced coordinate in reciprocal space.
            displ: displacement in real space of the atoms.
            eta: pre-factor multiplying the displacement. Gives the value in Angstrom of the largest displacement.
            frac_coords: whether the displacements are given in fractional or cartesian coordinates
            scale_matrix: the scaling matrix of the supercell. If None a scaling matrix suitable for
                the qpoint will be determined.
            max_supercell: mandatory if scale_matrix is None, ignored otherwise. Defines the largest
                supercell in the search for a scaling matrix suitable for the input q-point.

        Returns:
            A namedtuple with a Structure with the displaced atoms, a numpy array containing the
            displacements applied to each atom and the scale matrix used to generate the supercell.
        """

        if scale_matrix is None:
            if max_supercell is None:
                raise ValueError("If scale_matrix is not provided in input, please provide max_supercell!")
            scale_matrix = self.get_smallest_supercell(qpoint, max_supercell=max_supercell)

        scale_matrix = np.array(scale_matrix, np.int16)
        if scale_matrix.shape != (3, 3):
            scale_matrix = np.array(scale_matrix * np.eye(3), np.int16)
        #print("scale_matrix:\n", scale_matrix)

        old_lattice = self._lattice
        new_lattice = Lattice(np.dot(scale_matrix, old_lattice.matrix))

        tvects = self.get_trans_vect(scale_matrix)
        #print("tvects\n", tvects)

        if frac_coords:
            displ = np.array([old_lattice.get_cartesian_coords(d) for d in displ])
        else:
            displ = np.array(displ)

        # from here on, displ is in cartesian coordinates.
        displ = eta * displ / np.linalg.norm(displ, axis=1).max()

        new_displ = np.zeros(3, dtype=float)
        new_sites = []
        displ_list = []
        for iat, site in enumerate(self):
            for t in tvects:
                new_displ[:] = np.real(np.exp(2*1j*np.pi * (np.dot(qpoint, t))) * displ[iat,:])
                displ_list.append(list(new_displ))

                coords = site.coords + old_lattice.get_cartesian_coords(t) + new_displ
                new_site = PeriodicSite(
                    site.species, coords, new_lattice,
                    coords_are_cartesian=True, properties=site.properties,
                    to_unit_cell=True)
                new_sites.append(new_site)

        new_structure = self.__class__.from_sites(new_sites)

        return dict2namedtuple(structure=new_structure, displ=np.array(displ_list), scale_matrix=scale_matrix)

    def calc_kptbounds(self) -> np.array:
        """Returns the suggested value for the ABINIT variable ``kptbounds``."""
        kptbounds = [k.frac_coords for k in self.hsym_kpoints]
        return np.reshape(kptbounds, (-1, 3))

    def get_kpath_input_string(self, fmt: str = "abinit", line_density: int = 10) -> str:
        """
        Return string with input variables for band-structure calculations in the format used by code `fmt`.
        Use `line_density` points for the smallest segment (if supported by code).
        """
        lines = []; app = lines.append
        if fmt in ("abinit", "abivars"):
            app("# Abinit Structure")
            app(self.convert(fmt=fmt))
            app("\n# tolwfr 1e-20 iscf -2 # NSCF run")
            app('# To read previous DEN file, use: getden -1 or specify filename via getden_path "out_DEN"')
            app("\n# K-path in reduced coordinates:")
            app(" ndivsm %d" % line_density)
            app(" kptopt %d" % -(len(self.hsym_kpoints) - 1))
            app(" kptbounds")
            for k in self.hsym_kpoints:
                app("    {:+.5f}  {:+.5f}  {:+.5f}  # {kname}".format(*k.frac_coords, kname=k.name))

        elif fmt in ("wannier90", "w90"):
            app("# Wannier90 structure")
            from abipy.wannier90.win import Wannier90Input
            win = Wannier90Input(self)
            win.set_kpath()
            app(win.to_string())

        elif fmt == "siesta":
            app("# Siesta structure")
            app(self.convert(fmt=fmt))
            # Build normalized k-path.
            from .kpoints import Kpath
            vertices_names = [(k.frac_coords, k.name) for k in self.hsym_kpoints]
            kpath = Kpath.from_vertices_and_names(self, vertices_names, line_density=line_density)
            app("%block BandLines")
            prev_ik = 0
            for ik, k in enumerate(kpath):
                if not k.name: continue
                n = ik - prev_ik
                app("{}  {:+.5f}  {:+.5f}  {:+.5f}  # {kname}".format(n if n else 1, *k.frac_coords, kname=k.name))
                prev_ik = ik
            app("%endblock BandLines")

        else:
            raise ValueError("Don't know how to generate string for code: `%s`" % str(fmt))

        return "\n".join(lines)

    def calc_ksampling(self, nksmall, symprec=0.01, angle_tolerance=5) -> AttrDict:
        """
        Return the k-point sampling from the number of divisions ``nksmall`` to be used for
        the smallest reciprocal lattice vector.
        """
        ngkpt = self.calc_ngkpt(nksmall)
        shiftk = self.calc_shiftk(symprec=symprec, angle_tolerance=angle_tolerance)

        return AttrDict(ngkpt=ngkpt, shiftk=shiftk)

    def calc_ngkpt(self, nksmall) -> np.ndarray:
        """
        Compute the ABINIT variable ``ngkpt`` from the number of divisions used
        for the smallest lattice vector.

        Args:
            nksmall (int): Number of division for the smallest lattice vector.
        """
        lengths = self.lattice.reciprocal_lattice.abc
        lmin = np.min(lengths)

        ngkpt = np.ones(3, dtype=int)
        for i in range(3):
            ngkpt[i] = int(round(nksmall * lengths[i] / lmin))
            if ngkpt[i] == 0:
                ngkpt[i] = 1

        return ngkpt

    def calc_shiftk(self, symprec=0.01, angle_tolerance=5) -> np.ndarray:
        """
        Find the values of ``shiftk`` and ``nshiftk`` appropriated for the sampling of the Brillouin zone.

        When the primitive vectors of the lattice do NOT form a FCC or a BCC lattice,
        the usual (shifted) Monkhorst-Pack grids are formed by using nshiftk=1 and shiftk 0.5 0.5 0.5 .
        This is often the preferred k point sampling. For a non-shifted Monkhorst-Pack grid,
        use `nshiftk=1` and `shiftk 0.0 0.0 0.0`, but there is little reason to do that.

        When the primitive vectors of the lattice form a FCC lattice, with rprim::

                0.0 0.5 0.5
                0.5 0.0 0.5
                0.5 0.5 0.0

        the (very efficient) usual Monkhorst-Pack sampling will be generated by using nshiftk= 4 and shiftk::

            0.5 0.5 0.5
            0.5 0.0 0.0
            0.0 0.5 0.0
            0.0 0.0 0.5

        When the primitive vectors of the lattice form a BCC lattice, with rprim::

               -0.5  0.5  0.5
                0.5 -0.5  0.5
                0.5  0.5 -0.5

        the usual Monkhorst-Pack sampling will be generated by using nshiftk= 2 and shiftk::

                0.25  0.25  0.25
               -0.25 -0.25 -0.25

        However, the simple sampling nshiftk=1 and shiftk 0.5 0.5 0.5 is excellent.

        For hexagonal lattices with hexagonal axes, e.g. rprim::

                1.0  0.0       0.0
               -0.5  sqrt(3)/2 0.0
                0.0  0.0       1.0

        one can use nshiftk= 1 and shiftk 0.0 0.0 0.5
        In rhombohedral axes, e.g. using angdeg 3*60., this corresponds to shiftk 0.5 0.5 0.5,
        to keep the shift along the symmetry axis.

        Returns:
            Suggested value of shiftk.
        """
        # Find lattice type.
        sym = SpacegroupAnalyzer(self, symprec=symprec, angle_tolerance=angle_tolerance)
        lattice_type, spg_symbol = sym.get_lattice_type(), sym.get_space_group_symbol()

        # Check if the cell is primitive
        is_primitive = len(sym.find_primitive()) == len(self)

        # Generate the appropriate set of shifts.
        shiftk = None

        if is_primitive:
            if lattice_type == "cubic":
                if "F" in spg_symbol:
                    # FCC
                    shiftk = [0.5, 0.5, 0.5,
                              0.5, 0.0, 0.0,
                              0.0, 0.5, 0.0,
                              0.0, 0.0, 0.5]

                elif "I" in spg_symbol:
                    # BCC
                    shiftk = [0.25,  0.25,  0.25,
                             -0.25, -0.25, -0.25]
                    #shiftk = [0.5, 0.5, 05])

            elif lattice_type == "hexagonal":
                # Find the hexagonal axis and set the shift along it.
                for i, angle in enumerate(self.lattice.angles):
                    if abs(angle - 120) < 1.0:
                        j = (i + 1) % 3
                        k = (i + 2) % 3
                        hex_ax = [ax for ax in range(3) if ax not in [j,k]][0]
                        break
                else:
                    raise ValueError("Cannot find hexagonal axis")

                shiftk = [0.0, 0.0, 0.0]
                shiftk[hex_ax] = 0.5

            elif lattice_type == "tetragonal":
                if "I" in spg_symbol:
                    # BCT
                    shiftk = [0.25,  0.25,  0.25,
                             -0.25, -0.25, -0.25]

        if shiftk is None:
            # Use default value.
            shiftk = [0.5, 0.5, 0.5]

        return np.reshape(shiftk, (-1, 3))

    def num_valence_electrons(self, pseudos) -> float:
        """
        Returns the number of valence electrons.

        Args:
            pseudos: List of |Pseudo| objects or list of filenames.
        """
        from abipy.flowtk import PseudoTable
        nval, table = 0, PseudoTable.as_table(pseudos)
        for site in self:
            pseudo = table.pseudo_with_symbol(site.specie.symbol)
            nval += pseudo.Z_val

        return int(nval) if int(nval) == nval else nval

    def valence_electrons_per_atom(self, pseudos) -> list:
        """
        Returns the number of valence electrons for each atom in the structure.

        Args:
            pseudos: List of |Pseudo| objects or list of filenames.
        """
        from abipy.flowtk import PseudoTable
        table = PseudoTable.as_table(pseudos)
        psp_valences = []
        for site in self:
            pseudo = table.pseudo_with_symbol(site.specie.symbol)
            psp_valences.append(pseudo.Z_val)

        return psp_valences

    def write_notebook(self, nbpath=None) -> str:
        """
        Write a jupyter_ notebook to ``nbpath``. If nbpath is None, a temporay file in the current
        working directory is created. Return path to the notebook.
        """
        nbformat, nbv, nb = self.get_nbformat_nbv_nb(title=None)

        # Use pickle files for data persistence.
        # The notebook will reconstruct the object from this file
        _, tmpfile = tempfile.mkstemp(suffix='.pickle')
        with open(tmpfile, "wb") as fh:
            pickle.dump(self, fh)

        nb.cells.extend([
            #nbv.new_markdown_cell("# This is a markdown cell"),
            nbv.new_code_cell("structure = abilab.Structure.from_file('%s')" % tmpfile),
            nbv.new_code_cell("print(structure)"),
            nbv.new_code_cell("print(structure.abi_string)"),
            nbv.new_code_cell("structure"),
            nbv.new_code_cell("print(structure.spget_summary())"),
            nbv.new_code_cell("if structure.abi_spacegroup is not None: print(structure.abi_spacegroup)"),
            nbv.new_code_cell("print(structure.hsym_kpoints)"),
            nbv.new_code_cell("structure.plot_bz();"),
            nbv.new_code_cell("#import panel as pn; pn.extension()\n#structure.get_panel()"),
            nbv.new_code_cell("# sanitized = structure.abi_sanitize(); print(sanitized)"),
            nbv.new_code_cell("# ase_atoms = structure.to_ase_atoms()"),
            nbv.new_code_cell("# structure.plot_atoms();"),
            nbv.new_code_cell("# jsmol_view = structure.get_jsmol_view(); jsmol_view"),
            nbv.new_code_cell("# ngl_view = structure.get_ngl_view(); ngl_view"),
            nbv.new_code_cell("# ctk_view = structure.get_crystaltk_view(); ctk_view"),
        ])

        return self._write_nb_nbpath(nb, nbpath)


def dataframes_from_structures(struct_objects, index=None, symprec=1e-2, angle_tolerance=5,
                               with_spglib=True, cart_coords=False):
    """
    Build two pandas Dataframes_ with the most important geometrical parameters associated to
    a list of structures or a list of objects that can be converted into structures.

    Args:
        struct_objects: List of objects that can be converted to structure.
            Support filenames, structure objects, Abinit input files, dicts and many more types.
            See ``Structure.as_structure`` for the complete list.
        index: Index of the |pandas-DataFrame|.
        symprec (float): Symmetry precision used to refine the structure.
        angle_tolerance (float): Tolerance on angles.
        with_spglib (bool): If True, spglib_ is invoked to get the spacegroup symbol and number.
        cart_coords: True if the ``coords`` dataframe should contain Cartesian cordinates
            instead of Reduced coordinates.

    Return:
        namedtuple with two |pandas-DataFrames| named ``lattice`` and ``coords``
        ``lattice`` contains the lattice parameters. ``coords`` the atomic positions..
        The list of structures is available in the ``structures`` entry.

    .. code-block:: python

        dfs = dataframes_from_structures(files)
        dfs.lattice
        dfs.coords
        for structure in dfs.structures:
            print(structure)
    """
    structures = [Structure.as_structure(obj) for obj in struct_objects]
    # Build Frame with lattice parameters.
    # Use OrderedDict to have columns ordered nicely.
    odict_list = [(structure.get_dict4pandas(with_spglib=with_spglib, symprec=symprec,
                                             angle_tolerance=angle_tolerance)) for structure in structures]

    lattice_frame = pd.DataFrame(odict_list, index=index,
                                 columns=list(odict_list[0].keys()) if odict_list else None)

    # Build Frame with atomic positions.
    vtos = lambda v: "%+0.6f %+0.6f %+0.6f" % (v[0], v[1], v[2])
    max_numsite = max(len(s) for s in structures)
    odict_list = []
    for structure in structures:
        if cart_coords:
            odict_list.append({i: (site.species_string, vtos(site.coords)) for i, site in enumerate(structure)})
        else:
            odict_list.append({i: (site.species_string, vtos(site.frac_coords)) for i, site in enumerate(structure)})

    coords_frame = pd.DataFrame(odict_list, index=index,
                                columns=list(range(max_numsite)) if odict_list else None)

    return dict2namedtuple(lattice=lattice_frame, coords=coords_frame, structures=structures)


class StructureModifier:
    """
    This object provides an easy-to-use interface for
    generating new structures according to some algorithm.

    The main advantages of this approach are:

        *) Client code does not have to worry about the fact
           that many methods of Structure modify the object in place.

        *) One can render the interface more user-friendly. For example
           some arguments might have a unit that can be specified in input.
           For example one can pass a length in Bohr that will be automatically
           converted into Angstrom before calling the pymatgen methods
    """
    def __init__(self, structure: Structure):
        """
        Args:
            structure: Structure object.
        """
        # Get a copy to avoid any modification of the input.
        self._original_structure = structure.copy()

    def copy_structure(self) -> Structure:
        """Returns a copy of the original structure."""
        return self._original_structure.copy()

    def scale_lattice(self, vol_ratios: list) -> list:
        """
        Scale the lattice vectors so that length proportions and angles are preserved.

        Args:
            vol_ratios: List with the ratios v/v0 where v0 is the volume of the original structure.

        Return: List of new structures with desired volume.
        """
        vol_ratios = np.array(vol_ratios)
        new_volumes = self._original_structure.volume * vol_ratios

        news = []
        for vol in new_volumes:
            new_structure = self.copy_structure()
            new_structure.scale_lattice(vol)
            news.append(new_structure)

        return news

    def make_supercell(self, scaling_matrix) -> Structure:
        """
        Create a supercell.

        Args:
            scaling_matrix: A scaling matrix for transforming the lattice vectors.
                Has to be all integers. Several options are possible:

                a. A full 3x3 scaling matrix defining the linear combination of the old lattice vectors.
                    E.g., [[2,1,0],[0,3,0],[0,0,1]] generates a new structure with lattice vectors
                    a' = 2a + b, b' = 3b, c' = c
                    where a, b, and c are the lattice vectors of the original structure.
                b. A sequence of three scaling factors. e.g., [2, 1, 1]
                   specifies that the supercell should have dimensions 2a x b x c.
                c. A number, which simply scales all lattice vectors by the same factor.

        Returns:
            New structure.
        """
        new_structure = self.copy_structure()
        new_structure.make_supercell(scaling_matrix)
        return new_structure

    def displace(self, displ, etas, frac_coords=True):
        """
        Displace the sites of the structure along the displacement vector displ.

        The displacement vector is first rescaled so that the maxium atomic displacement
        is one Angstrom, and then multiplied by eta. Hence passing eta=0.001, will move
        all the atoms so that the maximum atomic displacement is 0.001 Angstrom.

        Args:
            displ: Displacement vector with 3*len(self) entries (fractional coordinates).
            eta: Scaling factor.
            frac_coords: Boolean stating whether the vector corresponds to fractional or cartesian coordinates.

        Returns:
            List of new structures with displaced atoms.
        """
        if not isinstance(etas, collections.abc.Iterable):
            etas = [etas]

        news = []
        for eta in etas:
            new_structure = self.copy_structure()
            new_structure.displace(displ, eta, frac_coords=frac_coords)
            news.append(new_structure)

        return news

    def frozen_phonon(self, qpoint, displ, eta=1, frac_coords=False, scale_matrix=None, max_supercell=None):

        return self._original_structure.frozen_phonon(qpoint, displ, eta, frac_coords, scale_matrix, max_supercell)

    def frozen_2phonon(self, qpoint, displ1, displ2, eta=1, frac_coords=False, scale_matrix=None, max_supercell=None):

        return self._original_structure.frozen_2phonon(qpoint, displ1, displ2, eta, frac_coords, scale_matrix,
                                                       max_supercell)


def diff_structures(structures, fmt="cif", mode="table", headers=(), file=sys.stdout):
    """
    Convert list of structure to string using format `fmt`, print diff to file `file`.

    Args:
        structures: List of structures or list of objects that can be converted into structure e.g. filepaths
        fmt: Any output format supported by `structure.to` method. Non-case sensitive.
        mode: `table` to show results in tabular form or `diff` to show differences with unified diff.
        headers: can be an explicit list of column headers Otherwise a headerless table is produced
        file: Output Stream
    """
    outs = [s.convert(fmt=fmt).splitlines() for s in map(Structure.as_structure, structures)]

    if mode == "table":
        from itertools import zip_longest  # Py3k
        from tabulate import tabulate
        table = [r for r in zip_longest(*outs, fillvalue=" ")]
        print(tabulate(table, headers=headers), file=file)

    elif mode == "diff":
        import difflib
        fromfile, tofile = "", ""
        for i in range(1, len(outs)):
            if headers: fromfile, tofile = headers[0], headers[i]
            diff = "\n".join(difflib.unified_diff(outs[0], outs[i], fromfile=fromfile, tofile=tofile))
            print(diff, file=file)

    else:
        raise ValueError(f"Unsupported {mode=}")


def structure2siesta(structure: Structure, verbose=0) -> str:
    """
    Return string with structural information in Siesta format from pymatgen structure

    Args:
        structure: AbiPy structure.
        verbose: Verbosity level.
    """

    if not structure.is_ordered:
        raise NotImplementedError("""\
Received disordered structure with partial occupancies that cannot be converted to a Siesta input
Please use OrderDisorderedStructureTransformation or EnumerateStructureTransformation
to build an appropriate supercell from partial occupancies or alternatively use the Virtual Crystal Approximation.""")

    species_by_znucl = structure.species_by_znucl

    lines = []
    app = lines.append
    app("NumberOfAtoms %d" % len(structure))
    app("NumberOfSpecies %d" % structure.n_elems)

    if verbose:
        app("# The species number followed by the atomic number, and then by the desired label")
    app("%block ChemicalSpeciesLabel")
    for itype, specie in enumerate(species_by_znucl):
        app("    %d %d %s" % (itype + 1, specie.number, specie.symbol))
    app("%endblock ChemicalSpeciesLabel")

    # Write lattice vectors.
    # Set small values to zero. This usually happens when the CIF file
    # does not give structure parameters with enough digits.
    lvectors = np.where(np.abs(structure.lattice.matrix) > 1e-8, structure.lattice.matrix, 0.0)
    app("LatticeConstant 1.0 Ang")
    app("%block LatticeVectors")
    for r in lvectors:
        app("    %.10f %.10f %.10f" % (r[0], r[1], r[2]))
    app("%endblock LatticeVectors")

    # Write atomic coordinates
    #% block AtomicCoordinatesAndAtomicSpecies
    #4.5000 5.0000 5.0000 1
    #5.5000 5.0000 5.0000 1
    #% endblock AtomicCoordinatesAndAtomicSpecies
    app("AtomicCoordinatesFormat Fractional")
    app("%block AtomicCoordinatesAndAtomicSpecies")
    for i, site in enumerate(structure):
        itype = species_by_znucl.index(site.specie)
        fc = np.where(np.abs(site.frac_coords) > 1e-8, site.frac_coords, 0.0)
        app("    %.10f %.10f %.10f %d" % (fc[0], fc[1], fc[2], itype + 1))
    app("%endblock AtomicCoordinatesAndAtomicSpecies")

    return "\n".join(lines)


class StructDiff:
    """
    Print difference among structures.
    """
    def __init__(self, labels: list[str], structures):
        """
        Args:
            labels: Labels associated to structures
            structures: List of structures or objects that can be converted to structures.
        """
        self.labels = labels
        self.structs = [Structure.as_structure(s) for s in structures]

        # Consistency check.
        if len(self.labels) != len(self.structs):
            raise ValueError("len(self.labels) != len(self.structs)")
        if len(self.labels) != len(self.labels):
            raise ValueError(f"Found duplicated entries in: {self.labels}")
        natom = len(self.structs[0])
        if any(len(s) != natom for s in self.structs):
            raise ValueError(f"structures have different number of atoms!")

    def del_label(self, label: str) -> None:
        """Remove entry associated to label."""
        for il, this_label in enumerate(self.labels):
            if label == this_label:
                del self.labels[il]
                del self.structs[il]

    def get_lattice_dataframe(self) -> pd.DataFrame:
        """
        Build dataframe with lattice parameters.
        """
        d_list = []
        for label, structure in zip(self.labels, self.structs):
            d = {"label": label}
            for i, k in enumerate(["a", "b", "c"]):
                d[k] = structure.lattice.abc[i]
            for i, k in enumerate(["alpha", "beta", "gamma"]):
                d[k] = structure.lattice.angles[i]
            d_list.append(d)

        return pd.DataFrame(d_list).set_index("label", inplace=False)

    def get_sites_dataframe(self, with_cart_coords=False) -> pd.DataFrame:
        """
        Build dataframe with site positions.
        """
        # Handle possible rigid shift.
        #shift_cart, shift_frac = np.zeros(3), np.zeros(3)
        #if allow_rigid_shift:
        #    site1, site2 = self.structs[0][0], self.structs[1][0]
        #    shift_cart = site2.coords - site1.coords
        #    shift_frac = site2.frac_coords - site1.frac_coords

        d_list = []
        natom = len(self.structs[0])
        for isite in range(natom):
            for label, structure in zip(self.labels, self.structs):
                site = structure[isite]
                d = {"label": label, "site_index": isite}
                for i, k in enumerate(["xred1", "xred2", "xred3"]):
                    d[k] = site.frac_coords[i]
                if with_cart_coords:
                    for i, k in enumerate(["xcart1", "xcart2", "xcart3"]):
                        d[k] = site.coords[i]
                d_list.append(d)

        return pd.DataFrame(d_list).set_index("label", inplace=False)

    def tabulate(self, only_lattice=False, allow_rigid_shift=True, with_cart_coords=False, file=sys.stdout) -> None:
        """
        Tabulate lattice parameters and atomic positions.

        Args:
            only_lattice:
            allow_rigid_shift:
            with_cart_coords:
            file: Output stream
        """
        # Compare lattices.
        df = self.get_lattice_dataframe()
        print("\nLattice parameters (Ang units):", file=file)
        print(df.to_string(), file=file)
        if only_lattice: return

        # Compare sites.
        natom = len(self.structs[0])
        if any(len(s) != natom for s in self.structs): return
        df = self.get_sites_dataframe(with_cart_coords=with_cart_coords)

        print("\nAtomic sites (Ang units):", file=file)
        print(df.to_string(), file=file)
        print("", file=file)

    #def diff(self, ref_label, with_cart_coords=False, file=sys.stdout) -> None:
    #    df = self.get_lattice_dataframe()
    #    df = self.get_sites_dataframe(with_cart_coords=with_cart_coords)
