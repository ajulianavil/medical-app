


function updateDiagnosisOptions() {
    document.getElementById('diagnosis_input').style.display = 'block';
    document.getElementById('diagnosis_label').style.display = 'block';


    var selectedMed = document.getElementById("med_input").value;
    var diagnosisInput = document.getElementById("diagnosis_input");


    // Clear existing options in the second select field
    diagnosisInput.innerHTML = "";

    // Create new options based on the selected value in the first select field
    switch (selectedMed) {
        case "hc_hadlock":
            document.getElementById('diagnosis_input').style.display = 'block';
            document.getElementById('diagnosis_label').style.display = 'block';
            addOption(diagnosisInput, "Macrocefalia", "macrocrania");
            addOption(diagnosisInput, "Microcefalia", "microcrania");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "bpd_hadlock":
            addOption(diagnosisInput, "Anormalidad por valor superior", "anormal-sup");
            addOption(diagnosisInput, "Anormalidad por valor inferior", "anormal-inf");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "csp":
            addOption(diagnosisInput, "Anormalidad por valor superior", "anormal-sup");
            addOption(diagnosisInput, "Anormalidad por valor inferior", "anormal-inf");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "cm":
            addOption(diagnosisInput, "Megacisterno", "megacisterno");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "vp":
            addOption(diagnosisInput, "Ventriculomegalia leve", "ventri-leve");
            addOption(diagnosisInput, "Ventriculomegalia moderada", "ventri-mod");
            addOption(diagnosisInput, "Ventriculomegalia severa", "ventri-sev");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "va":
            addOption(diagnosisInput, "Ventriculomegalia leve", "ventri-leve");
            addOption(diagnosisInput, "Ventriculomegalia moderada", "ventri-mod");
            addOption(diagnosisInput, "Ventriculomegalia severa", "ventri-sev");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "cereb_hill":
            addOption(diagnosisInput, "Hipoplasia cereberal", "hipoplasia");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "afi":
            addOption(diagnosisInput, "Oligohidramnios", "oligohidramnios");
            addOption(diagnosisInput, "Polihidramnios", "polihidramnios");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "efw":
            addOption(diagnosisInput, "Feto grande", "feto-grande");
            addOption(diagnosisInput, "Feto pequeño", "feto-pequeño");
            addOption(diagnosisInput, "R.C.I.U", "rciu");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "todas":
            document.getElementById('diagnosis_input').style.display = 'none';
            document.getElementById('diagnosis_label').style.display = 'none';

            addOption(diagnosisInput, "---", "todos");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "Macrocefalia", "macrocrania");
            addOption(diagnosisInput, "Microcefalia", "microcrania");
            addOption(diagnosisInput, "Anormalidad por valor superior", "anormal-sup");
            addOption(diagnosisInput, "Anormalidad por valor inferior", "anormal-inf");
            addOption(diagnosisInput, "Megacisterno", "megacisterno");
            addOption(diagnosisInput, "Ventriculomegalia leve", "ventri-leve");
            addOption(diagnosisInput, "Ventriculomegalia moderada", "ventri-mod");
            addOption(diagnosisInput, "Ventriculomegalia severa", "ventri-sev");
            addOption(diagnosisInput, "Hipoplasia cereberal", "hipoplasia");
            addOption(diagnosisInput, "Oligohidramnios", "oligohidramnios");
            addOption(diagnosisInput, "Polihidramnios", "polihidramnios");
            addOption(diagnosisInput, "Feto grande", "feto-grande");
            addOption(diagnosisInput, "Feto pequeño", "feto-pequeño");
            addOption(diagnosisInput, "R.C.I.U", "rciu");
            break;
        case "normal":
            addOption(diagnosisInput, "---", "todos");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "Macrocefalia", "macrocrania");
            addOption(diagnosisInput, "Microcefalia", "microcrania");
            addOption(diagnosisInput, "Anormalidad por valor superior", "anormal-sup");
            addOption(diagnosisInput, "Anormalidad por valor inferior", "anormal-inf");
            addOption(diagnosisInput, "Megacisterno", "megacisterno");
            addOption(diagnosisInput, "Ventriculomegalia leve", "ventri-leve");
            addOption(diagnosisInput, "Ventriculomegalia moderada", "ventri-mod");
            addOption(diagnosisInput, "Ventriculomegalia severa", "ventri-sev");
            addOption(diagnosisInput, "Hipoplasia cereberal", "hipoplasia");
            addOption(diagnosisInput, "Oligohidramnios", "oligohidramnios");
            addOption(diagnosisInput, "Polihidramnios", "polihidramnios");
            addOption(diagnosisInput, "Feto grande", "feto-grande");
            addOption(diagnosisInput, "Feto pequeño", "feto-pequeño");
            addOption(diagnosisInput, "R.C.I.U", "rciu");
            break;
        default:
            addOption(diagnosisInput, "Todos", "todas");
            break;
    }
}

function updateMedOptions() {
    var selectedDiagnosis = document.getElementById("diagnosis_input").value;
    if (selectedDiagnosis == 'todos') {
        document.getElementById('diagnosis_input').style.display = 'none';
        document.getElementById('diagnosis_label').style.display = 'none';

        document.getElementById("med_input").value = 'todas';
    }    
}

// Function to add an option to a select element
function addOption(selectElement, text, value) {
    var option = document.createElement("option");
    option.text = text;
    option.value = value;
    selectElement.add(option);
}

