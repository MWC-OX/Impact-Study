import numpy as np

def encode_inputs(
    menopaus, agegrp, density, race, bmi, agefirst,
    nrelbc, brstproc, lastmamm, surgmeno, hrt
):
    """
    Converts user input values to a NumPy array with dataset coding.
    
    Parameters:
        - menopaus: int (0 = premenopausal, 1 = postmenopausal, -1 = unknown)
        - agegrp: int (exact age, e.g., 52; -1 = unknown)
        - density: int (1-4; -1 = unknown)
        - race: str ("WHITE", "BLACK", "ASIAN", "OTHER/MIXED")
        - bmi: float (e.g., 27.3; -1 = unknown)
        - agefirst: int (age at first birth; -1 = nulliparous)
        - nrelbc: int (0, 1, 2, or more; -1 = unknown)
        - brstproc: int (0 = no, 1 = yes, -1 = unknown)
        - lastmamm: int (0 = negative, 1 = false positive, -1 = unknown)
        - surgmeno: int (0 = natural, 1 = surgical, -1 = unknown/not menopausal)
        - hrt: int (0 = no, 1 = yes, -1 = unknown/not menopausal)

    Returns:
        np.ndarray: Array of encoded values in dataset order.
    """
    
    # Encode menopause
    menopaus_code = 9 if menopaus == -1 else int(menopaus)
    if agegrp >= 55:
        menopaus_code = 1 

    # Encode age group
    if agegrp == -1:
        agegrp_code = 10
    else:
        age_bins = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
        agegrp_code = next((i + 1 for i, val in enumerate(age_bins) if agegrp < val), 10)

    # Encode density
    density_code = 9 if density == -1 else int(density)

    # Encode race
    race_map = {
        "WHITE": 1,
        "ASIAN": 2,
        "BLACK": 3,
        "OTHER/MIXED": 5
    }
    race_code = race_map.get(race.upper(), 9)

    # Encode BMI
    if bmi == -1:
        bmi_code = 9
    elif bmi <= 24.99:
        bmi_code = 1
    elif bmi <= 29.99:
        bmi_code = 2
    elif bmi <= 34.99:
        bmi_code = 3
    else:
        bmi_code = 4

    # Encode age at first birth
    if agefirst == -1:
        agefirst_code = 2  # nulliparous
    elif agefirst < 30:
        agefirst_code = 0
    else:
        agefirst_code = 1

    # Encode number of first degree relatives
    nrelbc_code = 9 if nrelbc == -1 else int(nrelbc)

    # Encode previous breast procedure
    brstproc_code = 9 if brstproc == -1 else int(brstproc)

    # Encode last mammogram result
    lastmamm_code = 9 if lastmamm == -1 else int(lastmamm)

    # Encode surgical menopause
    surgmeno_code = 9 if surgmeno == -1 else int(surgmeno)

    # Encode current hormone therapy
    hrt_code = 9 if hrt == -1 else int(hrt)

    if menopaus_code in [0, 9]:
        hrt_code = 9

    return np.array([
        menopaus_code,
        agegrp_code,
        density_code,
        race_code,
        bmi_code,
        agefirst_code,
        nrelbc_code,
        brstproc_code,
        lastmamm_code,
        surgmeno_code,
        hrt_code
    ])
