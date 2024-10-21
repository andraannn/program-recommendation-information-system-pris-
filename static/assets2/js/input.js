// PROGRESS BAR FUNCTIONS
// const nextButton = document.getElementById("next");
// const prevButton = document.getElementById("prev");
// const progressBarFront = document.querySelector(".progress-bar-front");
// const steps = document.querySelectorAll(".step");
// const forms = document.querySelectorAll(".form");
// let currentStep = 1;

// nextButton.addEventListener("click", () => {
//   currentStep++;
//   if (currentStep > steps.length) {
//     currentStep = steps.length;
//     handleSubmit(); // Submit all forms
//   }
//   updateProgress();
// });

// prevButton.addEventListener("click", () => {
//   currentStep--;
//   if (currentStep < 1) {
//     currentStep = 1;
//   }
//   updateProgress();
// });

// function updateProgress() {
//   steps.forEach((step, index) => {
//     if (index < currentStep) {
//       step.classList.add("checked");
//     } else {
//       step.classList.remove("checked");
//     }
//   });

//   const progressPercentage = ((currentStep - 1) / (steps.length - 1)) * 100;
//   progressBarFront.style.width = `${progressPercentage}%`;

//   prevButton.hidden = currentStep === 1;
//   nextButton.textContent = currentStep === steps.length ? "Submit" : "Next";

//   updateFormVisibility();
// }

// function updateFormVisibility() {
//   forms.forEach((form, index) => {
//     form.style.display = index + 1 === currentStep ? "block" : "none";
//   });
// }

// function handleSubmit() {
//   // Gather data from all forms
//   const formData = new FormData();
//   forms.forEach((form) => {
//     const inputs = form.querySelectorAll("input");
//     inputs.forEach((input) => {
//       formData.append(input.name, input.value); // Use input name as key
//     });
//   });

//   // For now, let's just log the form data
//   for (const [key, value] of formData.entries()) {
//     console.log(`${key}: ${value}`);
//   }

//   // Send data to server
//   fetch("/student/input", {
//     method: "POST",
//     body: formData,
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       console.log("Form submitted successfully:", data);
//     })
//     .catch((error) => {
//       console.error("Error submitting form:", error);
//     });
// }

// updateProgress();

//PROVINCE and CITIES FUNCTIONS

// Define cities for each province
const citiesByProvince = {
  Agusan_del_Norte: [
    "Cabadbaran City",
    "Buenavista",
    "Butuan City",
    "Kitcharao",
    "Magallanes",
    "Nasipit",
    "Carmen",
    "Tubay",
  ],
  Agusan_del_Sur: [
    "Sibagat",
    "San Luis",
    "Bunawan",
    "Bayugan City",
    "San Francisco",
    "Prosperidad",
    "Esperanza",
    "Trento",
    "Talacogon",
  ],
  Bukidnon: [
    "Manolo Fortich",
    "Maramag",
    "San Fernando",
    "Cabanglasan",
    "Valencia City",
    "Impasug-ong",
    "Quezon",
    "Don Carlos",
    "Malaybalay City",
  ],
  Cebu: ["Bantayan", "San Remigio", "Carcar"],
  Compostela_Valley_Province: ["Monkayo", "Compostela", "New Bataan"],
  Davao_del_Norte: ["Tagum City", "Asuncion"],
  Davao_del_Sur: ["Hagonoy", "Digos City", "Davao City", "Magsaysay"],
  Dinagat_Islands: ["Cagdianao"],
  Laguna: ["Los Baños"],
  Lanao_del_Norte: [
    "Linamon",
    "Munai",
    "Pantao Ragat",
    "Kolambugan",
    "Matungao",
    "Pantar",
    "Sapad",
    "Kauswagan",
    "Bacolod",
    "Magsaysay",
    "Poona Piagapo",
    "Iligan City",
    "Tagoloan",
    "Salvador",
    "Tubod",
    "Lala",
    "Baroy",
    "Linamon",
    "Balo-i",
    "Kapatagan",
    "Sultan Naga Dimaporo",
    "Maigo",
  ],
  Lanao_del_Sur: [
    "Lumba Bayabao",
    "Bubong",
    "Balabagan",
    "Malabang",
    "Tubaran",
    "Balindong",
    "Pualas",
    "Marawi City",
    "Poona Bayabao",
    "Saguiaran",
    "Pagayawan",
    "Wao",
    "Marantao",
  ],
  Leyte: ["Isabel"],
  Maguindanao: ["Cotabato City", "Datu Odin Sinsuat", "Midsayap"],
  Metro_Manila: ["Caloocan City"],
  Misamis_Occidental: [
    "Oroquieta City",
    "Ozamiz City",
    "Sinacaban",
    "Jimenez",
    "Tangub City",
    "Clarin",
    "Tudela",
    "Lopez Jaena",
    "Aloran",
    "Ozamis City",
    "Calamba",
    "Bonifacio",
    "Sapang Dalaga",
    "Plaridel",
    "Baliangao",
    "Panaon",
  ],
  Misamis_Oriental: [
    "Alubijid",
    "Manticao",
    "Gitagum",
    "Medina",
    "Jasaan",
    "Claveria",
    "Cagayan de Oro City",
    "Lugait",
    "Initao",
    "Talisayan",
    "El Salvador",
    "Gingoog City",
    "Balingasag",
    "Naawan",
    "Laguindingan",
    "Tagoloan",
    "El Salvador City",
    "Opol",
  ],
  Negros_Occidental: ["Bacolod City"],
  North_Cotabato: ["Pigcawayan", "Kidapawan City", "Banisilan", "Midsayap"],
  Siquijor: ["Lazi"],
  South_Cotabato: [
    "Polomolok",
    "General Santos City",
    "Banga",
    "Koronadal City",
  ],
  Sultan_Kudarat: ["Lebak", "Esperanza", "Isulan"],
  Sulu: ["Jolo"],
  Surigao_del_Norte: [
    "Pilar",
    "Bacuag",
    "Surigao City",
    "Sison",
    "Gigaquit",
    "Claver",
    "Placer",
    "Mainit",
  ],
  Surigao_del_Sur: [
    "Cagwait",
    "Tagbina",
    "Cantilan",
    "Cortes",
    "Bislig City",
    "Carrascal",
    "Lingig",
    "San Agustin",
    "Carmen",
    "Barobo",
    "Tandag City",
    "Hinatuan",
  ],
  Tawi_Tawi: ["Bongao"],
  Zamboanga_Sibugay: [
    "Diplahan",
    "Alicia",
    "Imelda",
    "Malangas",
    "Buug",
    "Siay",
  ],
  Zamboanga_del_Norte: [
    "Sergio Osmena Sr.",
    "Sindangan",
    "Siocon",
    "Salug",
    "Godod",
    "Dipolog City",
    "Katipunan",
    "Polanco",
    "Labason",
  ],
  Zamboanga_del_Sur: [
    "Ramon Magsaysay",
    "Sominot",
    "Labangan",
    "San Pablo",
    "Pagadian City",
    "Tabina",
    "Margosatubig",
    "Aurora",
    "Molave",
    "Lakewood",
    "Dumingag",
    "Zamboanga City",
    "Mahayag",
    "Josefina",
    "Dimataling",
    "Dumalinao",
    "Guipos",
    "Midsalip",
    "Kumalarang",
    "Vincenzo Sagun",
    "Tambulig",
    "Dinas",
    "Lapuyan",
    "Tukuran",
  ],
};

// Function to update the city dropdown based on the selected province
function updateCities() {
  const provinceDropdown = document.getElementById("province_home");
  const cityDropdown = document.getElementById("city_home");
  const selectedProvince = provinceDropdown.value;

  // Clear previous city options
  cityDropdown.innerHTML = '<option value="">-- Select City --</option>';

  // Populate city dropdown based on the selected province
  if (selectedProvince && citiesByProvince[selectedProvince]) {
    citiesByProvince[selectedProvince].forEach((city) => {
      const option = document.createElement("option");
      option.value = city;
      option.textContent = city;
      cityDropdown.appendChild(option);
    });
  }
}

// IN CASE HIDE CITY FIRST WILL BE USED

// function updateCities() {
//   const provinceDropdown = document.getElementById("province_home");
//   const cityDropdownContainer = document.getElementById("city_home_container");
//   const cityDropdown = document.getElementById("city_home");
//   const selectedProvince = provinceDropdown.value;

//   // Clear previous city options
//   cityDropdown.innerHTML = '<option value="">-- Select City --</option>';

//   // Show or hide the city dropdown container based on province selection
//   if (selectedProvince && citiesByProvince[selectedProvince]) {
//     cityDropdownContainer.style.display = "block"; // Show city dropdown container
//     citiesByProvince[selectedProvince].forEach((city) => {
//       const option = document.createElement("option");
//       option.value = city;
//       option.textContent = city;
//       cityDropdown.appendChild(option);
//     });
//   } else {
//     cityDropdownContainer.style.display = "none"; // Hide city dropdown container
//   }
// }

//TRACK TO SUBJECTS FUNCTIONS

const subjects = {
  STEM: [
    "EarthAndLifeScience",
    "PhysicalScience",
    "EarthScience",
    "GenBio1",
    "GenBio2",
    "GenPhysics1",
    "GenPhysics2",
    "GenChem1",
    "GenChem2",
    "GeneralMath",
    "StatisticsAndProbability",
    "PreCalculus",
    "BasicCalculus",

    "OralCommunication",
    "Reading_and_Writing",
    "MediaandInformationLiteracy",
    "t21stCenturyLiteratureFromThePhilippinesAndTheWorld",
    "ContemporaryPhilippineArtsFromTheRegions",

    "PagbasaAtPagsusuriNgIbatIbangTekstoTungoSaPananaliksik",
    "KomunikasyonAtPananaliksikSaWikaAtKulturangPilipino",
    "PersonalDevelopment",
    "IntroductionToThePhilosophyOfTheHumanPerson",
    "UnderstandingCultureSocietyAndPolitics",
    "DisasterReadinessAndRisk_Reduction",
    "PhysicalEducationAndHealth",
    "PhysicalEducationAndHealth2",
    "PhysicalEducationandHealth3",
    "PhysicalEducationAndHealth4",
  ],
  ABM: [
    "EarthAndLifeScience",
    "PhysicalScience",
    "EarthScience",

    "GeneralMath",
    "StatisticsAndProbability",
    "BusinessMath",
    "BusinessFinance",

    "OralCommunication",
    "Reading_and_Writing",
    "MediaandInformationLiteracy",
    "t21stCenturyLiteratureFromThePhilippinesAndTheWorld",
    "ContemporaryPhilippineArtsFromTheRegions",

    "PagbasaAtPagsusuriNgIbatIbangTekstoTungoSaPananaliksik",
    "KomunikasyonAtPananaliksikSaWikaAtKulturangPilipino",
    "PersonalDevelopment",
    "IntroductionToThePhilosophyOfTheHumanPerson",
    "UnderstandingCultureSocietyAndPolitics",
    "DisasterReadinessAndRisk_Reduction",
    "PhysicalEducationAndHealth",
    "PhysicalEducationAndHealth2",
    "PhysicalEducationandHealth3",
    "PhysicalEducationAndHealth4",
    "OrganizationAndManagement",
    "PrinciplesOfMarketing",
    "BusinessMarketing",
    "BusinessEnterpriseAndSimulation",
    "F1_FundamentalsOfAccountancyBusinessAndManagement1",
    "F2_FundamentalsofAccountancyBusinessAndManagement2",
    "AppliedEconomicsBusiness",
    "EthicsAndSocial_Responsibility",
  ],
  HUMSS: [
    "EarthAndLifeScience",
    "PhysicalScience",
    "EarthScience",

    "GeneralMath",
    "StatisticsAndProbability",
    "OralCommunication",
    "Reading_and_Writing",
    "MediaandInformationLiteracy",
    "t21stCenturyLiteratureFromThePhilippinesAndTheWorld",
    "ContemporaryPhilippineArtsFromTheRegions",
    "CreativeNonfiction",

    "PagbasaAtPagsusuriNgIbatIbangTekstoTungoSaPananaliksik",
    "KomunikasyonAtPananaliksikSaWikaAtKulturangPilipino",

    "CreativeWriting_Malikhaing_Pagsulat",

    "PersonalDevelopment",
    "IntroductionToThePhilosophyOfTheHumanPerson",
    "UnderstandingCultureSocietyAndPolitics",
    "DisasterReadinessAndRisk_Reduction",
    "PhysicalEducationAndHealth",
    "PhysicalEducationAndHealth2",
    "PhysicalEducationandHealth3",
    "PhysicalEducationAndHealth4",
    "IntroductionToWorldReligionsAndBeliefSystems",
    "Community_EngagementSolidarityAndCitizenship",
    "PhilippinePoliticsandGovernance",
    "DisciplinesAndIdeasInTheSocialSciences",
  ],
  GAS: [
    "EarthAndLifeScience",
    "PhysicalScience",
    "EarthScience",

    "GeneralMath",
    "StatisticsAndProbability",

    "OralCommunication",
    "Reading_and_Writing",
    "MediaandInformationLiteracy",
    "t21stCenturyLiteratureFromThePhilippinesAndTheWorld",
    "ContemporaryPhilippineArtsFromTheRegions",
    "CreativeWriting",

    "PagbasaAtPagsusuriNgIbatIbangTekstoTungoSaPananaliksik",
    "KomunikasyonAtPananaliksikSaWikaAtKulturangPilipino",

    "PersonalDevelopment",
    "IntroductionToThePhilosophyOfTheHumanPerson",
    "UnderstandingCultureSocietyAndPolitics",
    "DisasterReadinessAndRisk_Reduction",
    "PhysicalEducationAndHealth",
    "PhysicalEducationAndHealth2",
    "PhysicalEducationandHealth3",
    "PhysicalEducationAndHealth4",
    "Humanities1_Politics",
    "Humanities2_intro",
    "SocialScience1",
    "OrganizationAndManagement2",
    "AppliedEconomics2",
    "IntroToWorldReligionsAndSytemBeliefs",
    "PhilippinePiliticsAndGovernance",
  ],
  TVL: [
    "EarthAndLifeScience",
    "PhysicalScience",
    "EarthScience",

    "GeneralMath",
    "StatisticsAndProbability",

    "OralCommunication",
    "Reading_and_Writing",
    "MediaandInformationLiteracy",
    "t21stCenturyLiteratureFromThePhilippinesAndTheWorld",
    "ContemporaryPhilippineArtsFromTheRegions",
    "CreativeWriting",

    "PagbasaAtPagsusuriNgIbatIbangTekstoTungoSaPananaliksik",
    "KomunikasyonAtPananaliksikSaWikaAtKulturangPilipino",

    "PersonalDevelopment",
    "IntroductionToThePhilosophyOfTheHumanPerson",
    "UnderstandingCultureSocietyAndPolitics",
    "DisasterReadinessAndRisk_Reduction",
    "PhysicalEducationAndHealth",
    "PhysicalEducationAndHealth2",
    "PhysicalEducationandHealth3",
    "PhysicalEducationAndHealth4",
    "SafetyAndFirstAid",
    "HumanMovement",
    "FundamentalsOfCoaching",
  ],
};

// Function to generate input fields for subjects
// Function to generate input fields for subjects
function generateSubjectInputs(track) {
  const subjectInputsContainer = document.getElementById("subjectInputs");
  subjectInputsContainer.innerHTML = ""; // Clear previous inputs

  const trackSubjects = subjects[track];
  if (trackSubjects) {
    trackSubjects.forEach((subject) => {
      const inputDiv = document.createElement("div");
      inputDiv.className = "mb-3";

      const inputField = document.createElement("input");
      inputField.type = "number";
      inputField.className = "form-control form-control-sm";
      inputField.name = subject;
      inputField.id = subject; // Assign an ID for FormData
      inputField.placeholder = subject.replace(/([A-Z])/g, " $1").trim();
      inputField.style.width = "300px";

      const label = document.createElement("label");
      label.htmlFor = subject;
      label.textContent = subject.replace(/([A-Z])/g, " $1").trim() + " Grade:";

      inputDiv.appendChild(label);
      inputDiv.appendChild(inputField);

      subjectInputsContainer.appendChild(inputDiv);
    });
  }
}

// Listen for changes in the track selection
let trackSelect = document.getElementById("track");
trackSelect.addEventListener("change", function () {
  let selectedTrack = this.value;
  generateSubjectInputs(selectedTrack);
});

// Initially hide all inputs
generateSubjectInputs("");

function handleSubmit() {
  // Create a new FormData object
  const formData = new FormData(document.getElementById("studentForm"));

  // Log the form data
  for (const [key, value] of formData.entries()) {
    console.log(`${key}: ${value}`);
  }

  // Send form data to server using fetch
  fetch("/student/input", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        console.log("Form submitted successfully");
        // Optionally, you can redirect to another page or show a success message here
      } else {
        console.error("Form submission failed");
        // Handle form submission failure
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
