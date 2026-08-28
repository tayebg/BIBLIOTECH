import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sources_dir = os.path.join(base_dir, "sources")
if sources_dir not in sys.path:
    sys.path.insert(0, sources_dir)

from BIBLIOTECH import Lim, Edit_Nb_Auteur

def test_lim_function():
    assert Lim("Short text", 1) == "Short text"
    long_text = "A" * 100
    assert len(Lim(long_text, 1)) == 65 + 3
    assert Lim(None, 1) == ""

def test_edit_nb_auteur():
    assert Edit_Nb_Auteur("Camus") == "Camus"
    assert Edit_Nb_Auteur("''") == "''"
    assert Edit_Nb_Auteur("") == ""
