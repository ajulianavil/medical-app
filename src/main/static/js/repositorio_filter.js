


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
            addOption(diagnosisInput, "Macrocrania", "macrocrania");
            addOption(diagnosisInput, "Microcefalia", "microcefalia");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "bpd_hadlock":
            addOption(diagnosisInput, "Anormalidad por valor superior", "Anormalidad por valor superior");
            addOption(diagnosisInput, "Anormalidad por valor inferior", "Anormalidad por valor inferior");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "csp":
            addOption(diagnosisInput, "Anormalidad por valor superior", "Anormalidad por valor superior");
            addOption(diagnosisInput, "Anormalidad por valor inferior", "Anormalidad por valor inferior");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "cm":
            addOption(diagnosisInput, "Megacisterno", "Megacisterno o cisterno alargada");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "vp":
            addOption(diagnosisInput, "Ventriculomegalia leve", "Ventriculomegalia leve");
            addOption(diagnosisInput, "Ventriculomegalia moderada", "Ventriculomegalia moderada");
            addOption(diagnosisInput, "Ventriculomegalia severa", "Ventriculomegalia severa");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "va":
            addOption(diagnosisInput, "Ventriculomegalia leve", "Ventriculomegalia leve");
            addOption(diagnosisInput, "Ventriculomegalia moderada", "Ventriculomegalia moderada");
            addOption(diagnosisInput, "Ventriculomegalia severa", "Ventriculomegalia severa");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "cereb_hill":
            addOption(diagnosisInput, "Hipoplasia cereberal", "Hipoplasia cereberal");
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
            addOption(diagnosisInput, "Feto grande", "Feto grande para la edad gestacional");
            addOption(diagnosisInput, "Feto pequeño", "Feto pequeño para la edad gestacional");
            addOption(diagnosisInput, "R.C.I.U", "R.C.I.U (Restricción del crecimiento interuterino)");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "---", "todos");
            break;
        case "todas":
            document.getElementById('diagnosis_input').style.display = 'none';
            document.getElementById('diagnosis_label').style.display = 'none';

            addOption(diagnosisInput, "---", "todos");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "Macrocrania", "macrocrania");
            addOption(diagnosisInput, "Microcefalia", "microcefalia");
            addOption(diagnosisInput, "Anormalidad por valor superior", "Anormalidad por valor superior");
            addOption(diagnosisInput, "Anormalidad por valor inferior", "Anormalidad por valor inferior");
            addOption(diagnosisInput, "Megacisterno", "megacisterno");
            addOption(diagnosisInput, "Ventriculomegalia leve", "Ventriculomegalia leve");
            addOption(diagnosisInput, "Ventriculomegalia moderada", "Ventriculomegalia moderada");
            addOption(diagnosisInput, "Ventriculomegalia severa", "Ventriculomegalia severa");
            addOption(diagnosisInput, "Hipoplasia cereberal", "Hipoplasia cereberal");
            addOption(diagnosisInput, "Oligohidramnios", "oligohidramnios");
            addOption(diagnosisInput, "Polihidramnios", "polihidramnios");
            addOption(diagnosisInput, "Feto grande", "Feto grande para la edad gestacional");
            addOption(diagnosisInput, "Feto pequeño", "Feto pequeño para la edad gestacional");
            addOption(diagnosisInput, "R.C.I.U", "R.C.I.U (Restricción del crecimiento interuterino)");
            break;
        case "normal":
            addOption(diagnosisInput, "---", "todos");
            addOption(diagnosisInput, "Normal", "normal");
            addOption(diagnosisInput, "Macrocrania", "macrocrania");
            addOption(diagnosisInput, "Microcefalia", "microcefalia");
            addOption(diagnosisInput, "Anormalidad por valor superior", "Anormalidad por valor superior");
            addOption(diagnosisInput, "Anormalidad por valor inferior", "Anormalidad por valor inferior");
            addOption(diagnosisInput, "Megacisterno", "megacisterno");
            addOption(diagnosisInput, "Ventriculomegalia leve", "Ventriculomegalia leve");
            addOption(diagnosisInput, "Ventriculomegalia moderada", "Ventriculomegalia moderada");
            addOption(diagnosisInput, "Ventriculomegalia severa", "Ventriculomegalia severa");
            addOption(diagnosisInput, "Hipoplasia cereberal", "Hipoplasia cereberal");
            addOption(diagnosisInput, "Oligohidramnios", "oligohidramnios");
            addOption(diagnosisInput, "Polihidramnios", "polihidramnios");
            addOption(diagnosisInput, "Feto grande", "Feto grande para la edad gestacional");
            addOption(diagnosisInput, "Feto pequeño", "Feto pequeño para la edad gestacional");
            addOption(diagnosisInput, "R.C.I.U", "R.C.I.U (Restricción del crecimiento interuterino)");
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

