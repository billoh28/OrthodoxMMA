import sys, os
sys.path.insert(1, os.getcwd() + '/../')
from jab_classifier import generate_jab_feedback

def test_generate_jab_feedback_1():
    # The result from prediction:
        # 0 is correct
        # 1 is incorrect
    AP_pred_test = {"0": 0, "1": 1 }
    CP_pred_test = {"0": 2, "1": 2 }
    EO_pred_test = {"0": 0, "1": 1 }
    OC_pred_test = {"0": 3, "1": 1 }
    RE_pred_test = {"0": 0, "1": 4 } 

    report = generate_jab_feedback(AP_pred_test, CP_pred_test, EO_pred_test, OC_pred_test, RE_pred_test)

    expected_report = {
        "1": 2,
        "2": 2,
        "3": 2,
        "4": 2,
        "5": 2,
    }

    # To little predictions, should be over 5

    assert report == expected_report

def test_generate_jab_feedback_2():
    # The result from prediction:
        # 0 is correct
        # 1 is incorrect
    AP_pred_test = {"0": 0, "1": 100 }
    CP_pred_test = {"0": 40, "1": 8 }
    EO_pred_test = {"0": 100, "1": 10 }
    OC_pred_test = {"0": 10, "1": 10 }
    RE_pred_test = {"0": 0, "1": 4 } 

    report = generate_jab_feedback(AP_pred_test, CP_pred_test, EO_pred_test, OC_pred_test, RE_pred_test)

    expected_report = {
        "1": 0,
        "2": 1,
        "3": 1,
        "4": 0,
        "5": 2,
    }
    assert report == expected_report

def test_generate_jab_feedback_3():
    # The result from prediction:
        # 0 is correct
        # 1 is incorrect
    AP_pred_test = {"0": 100, "1": 0 }
    CP_pred_test = {"0": 100, "1": 0 }
    EO_pred_test = {"0": 1, "1": 100 }
    OC_pred_test = {"0": 119, "1": 120 }
    RE_pred_test = {"0": 20, "1": 10 } 

    report = generate_jab_feedback(AP_pred_test, CP_pred_test, EO_pred_test, OC_pred_test, RE_pred_test)

    expected_report = {
        "1": 1,
        "2": 1,
        "3": 0,
        "4": 0,
        "5": 1,
    }
    assert report == expected_report