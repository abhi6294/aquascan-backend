<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AquaPath AI • Clinical Diagnostics & Pathology Workstation</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        clinical: {
                            50: '#f0fdfa',
                            500: '#0d9488',
                            600: '#0f766e',
                        },
                        cyan: {
                            400: '#22d3ee',
                            500: '#06b6d4',
                            950: '#083344',
                        },
                        dark: {
                            950: '#050811',
                            900: '#0b1120',
                            850: '#0f172a',
                            800: '#1e293b',
                            700: '#334155'
                        }
                    },
                    fontFamily: {
                        sans: ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    }
                }
            }
        }
    </script>

    <style>
        .glass-panel {
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glow-accent {
            box-shadow: 0 0 25px -4px rgba(6, 182, 212, 0.2);
        }
        .spinner {
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-top: 2px solid #06b6d4;
            border-radius: 50%;
            width: 16px;
            height: 16px;
            animation: spin 0.7s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="bg-dark-950 text-slate-100 font-sans antialiased min-h-screen selection:bg-cyan-500 selection:text-black">

    <!-- Top Clinical Bar -->
    <header class="glass-panel border-b border-white/10 sticky top-0 z-50 px-4 lg:px-8 py-3.5">
        <div class="max-w-[1550px] mx-auto flex flex-wrap items-center justify-between gap-4">
            
            <div class="flex items-center space-x-3.5">
                <div class="p-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
                    <i data-lucide="microscope" class="w-6 h-6"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <span class="font-extrabold text-lg tracking-tight text-white">AquaPath<span class="text-cyan-400"> Clinical</span></span>
                        <span class="px-2 py-0.5 text-[10px] font-mono uppercase bg-cyan-950 text-cyan-300 border border-cyan-800 rounded font-semibold">Diagnostic Terminal</span>
                    </div>
                    <p class="text-xs text-slate-400">Automated Piscine Pathological Classification & Therapeutic Formulations</p>
                </div>
            </div>

            <!-- Server Telemetry Badges -->
            <div class="flex items-center gap-4 text-xs font-mono">
                <div class="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-dark-900 border border-white/5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="text-slate-300">Endpoint: Render Cloud (Online)</span>
                </div>
                <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-dark-900 border border-white/5 text-slate-400">
                    <i data-lucide="cpu" class="w-3.5 h-3.5 text-cyan-400"></i>
                    <span>EfficientNetB0 Backbone</span>
                </div>
                <a href="index.html" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-dark-800 hover:bg-dark-700 text-slate-200 border border-white/10 transition flex items-center gap-1.5">
                    <i data-lucide="arrow-left" class="w-3.5 h-3.5"></i>
                    <span>Back to Paper</span>
                </a>
            </div>

        </div>
    </header>

    <!-- Main Workstation Layout -->
    <main class="max-w-[1550px] mx-auto px-4 lg:px-8 py-6">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- LEFT WORKSTATION: Specimen Intake & Vision (5 Columns) -->
            <div class="lg:col-span-5 flex flex-col gap-5">
                
                <!-- Specimen Intake Area -->
                <div class="glass-panel p-5 rounded-2xl border border-white/10 glow-accent">
                    <div class="flex items-center justify-between mb-4 pb-3 border-b border-white/5">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-300 font-mono flex items-center gap-2">
                            <i data-lucide="upload" class="w-4 h-4 text-cyan-400"></i> Specimen Acquisition
                        </span>
                        <span id="specimenBadge" class="text-[10px] font-mono text-slate-500 uppercase">Awaiting Sample</span>
                    </div>

                    <div id="dropZone" class="relative border-2 border-dashed border-slate-700 hover:border-cyan-500/60 rounded-xl p-6 text-center bg-dark-900/60 transition cursor-pointer flex flex-col items-center justify-center min-h-[170px]">
                        <input type="file" id="specimenInput" accept="image/*" class="absolute inset-0 opacity-0 cursor-pointer w-full h-full">
                        <div id="dropContent" class="flex flex-col items-center gap-2">
                            <div class="w-12 h-12 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 flex items-center justify-center">
                                <i data-lucide="scan-line" class="w-6 h-6"></i>
                            </div>
                            <div>
                                <span class="text-xs font-semibold text-slate-200 block">Select specimen image or drag & drop</span>
                                <span class="text-[10px] text-slate-400 font-mono">Format: High-Res JPG, PNG, WEBP (Aquaculture specimen)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Dual Viewport Inspection Deck -->
                <div class="glass-panel p-5 rounded-2xl border border-white/10">
                    <div class="flex items-center justify-between mb-4 pb-3 border-b border-white/5">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-300 font-mono flex items-center gap-2">
                            <i data-lucide="layers" class="w-4 h-4 text-cyan-400"></i> Comparative Viewport
                        </span>
                        <span class="text-[10px] font-mono text-slate-400">Grad-CAM Spatial Heatmap</span>
                    </div>

                    <div class="grid grid-cols-2 gap-3.5">
                        <!-- Input Specimen -->
                        <div class="flex flex-col gap-1.5">
                            <div class="relative bg-dark-950 rounded-xl border border-white/10 overflow-hidden aspect-square flex items-center justify-center">
                                <img id="origViewer" src="" alt="Specimen Raw" class="w-full h-full object-cover hidden">
                                <div id="origBlank" class="text-center p-3 text-slate-600">
                                    <i data-lucide="image" class="w-8 h-8 mx-auto mb-1 opacity-50"></i>
                                    <span class="text-[10px] font-mono block">Raw Specimen View</span>
                                </div>
                                <span class="absolute bottom-2 left-2 px-2 py-0.5 rounded text-[9px] font-mono bg-black/80 text-slate-300 border border-white/10">INPUT SPECIMEN</span>
                            </div>
                            <span class="text-[10px] text-slate-400 text-center font-mono" id="origResolution">-- × -- px</span>
                        </div>

                        <!-- Heatmap Overlay -->
                        <div class="flex flex-col gap-1.5">
                            <div class="relative bg-dark-950 rounded-xl border border-white/10 overflow-hidden aspect-square flex items-center justify-center">
                                <img id="camViewer" src="" alt="Grad-CAM Saliency" class="w-full h-full object-cover hidden">
                                <div id="camBlank" class="text-center p-3 text-slate-600">
                                    <i data-lucide="eye" class="w-8 h-8 mx-auto mb-1 opacity-50"></i>
                                    <span class="text-[10px] font-mono block">Lesion Saliency View</span>
                                </div>
                                <span class="absolute bottom-2 left-2 px-2 py-0.5 rounded text-[9px] font-mono bg-black/80 text-cyan-300 border border-cyan-500/30">GRAD-CAM ATTRIBUTION</span>
                            </div>
                            <span class="text-[10px] text-slate-400 text-center font-mono">Focal Tissue Gradient</span>
                        </div>
                    </div>

                    <!-- Trigger Inference Button -->
                    <button id="diagnoseBtn" disabled
                            class="w-full mt-4 py-3.5 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 disabled:opacity-40 disabled:cursor-not-allowed text-slate-950 font-bold text-xs uppercase tracking-wider transition-all shadow-lg flex items-center justify-center gap-2">
                        <i data-lucide="play" class="w-4 h-4 fill-current"></i>
                        <span>Execute Pathological Inference</span>
                    </button>
                </div>

                <!-- Pathology Metadata Reference -->
                <div class="glass-panel p-4 rounded-xl border border-white/5 text-[11px] text-slate-400 font-mono space-y-1.5">
                    <div class="flex justify-between">
                        <span>Classification Model:</span>
                        <span class="text-slate-200">EfficientNetB0 (ImageNet Fine-Tuned)</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Target Spatial Layer:</span>
                        <span class="text-cyan-400">top_conv (Final Feature Block)</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Inference Latency:</span>
                        <span id="latencyTimer" class="text-emerald-400">0.00 ms</span>
                    </div>
                </div>

            </div>

            <!-- RIGHT WORKSTATION: Diagnostics & Medical Formulations (7 Columns) -->
            <div class="lg:col-span-7 flex flex-col gap-5">
                
                <!-- Clinical Diagnosis Hero -->
                <div id="diagCard" class="glass-panel p-6 rounded-2xl border border-white/10 glow-accent relative overflow-hidden">
                    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-white/10">
                        <div>
                            <div class="flex items-center gap-2 mb-1">
                                <span id="severityBadge" class="px-2.5 py-0.5 rounded text-[10px] font-mono uppercase font-bold bg-slate-800 text-slate-400 border border-white/10">
                                    Status: Standby
                                </span>
                                <span class="text-xs text-slate-400 font-mono">Primary Diagnostic Conclusion</span>
                            </div>
                            <h2 id="diagnosisTitle" class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Awaiting Analysis</h2>
                        </div>
                        
                        <div class="sm:text-right">
                            <span class="text-[10px] uppercase font-mono text-slate-400 block mb-0.5">Classification Confidence</span>
                            <div id="diagnosisScore" class="text-3xl font-extrabold font-mono text-slate-600">00.00%</div>
                        </div>
                    </div>

                    <!-- Softmax Distribution -->
                    <div class="mt-4">
                        <span class="text-xs font-semibold uppercase tracking-wider text-slate-300 font-mono block mb-3">
                            Class Probability Distribution Across 7 Pathologies
                        </span>
                        <div id="probBarContainer" class="space-y-2.5">
                            <div class="text-center py-6 text-xs text-slate-500 font-mono">
                                No diagnostic data loaded. Run inference to evaluate class distribution.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Structured Pharmacopeia & Treatment Plan -->
                <div class="glass-panel p-6 rounded-2xl border border-white/10 flex flex-col gap-4">
                    <div class="flex items-center justify-between pb-3 border-b border-white/5">
                        <h3 class="text-sm font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
                            <i data-lucide="pill" class="w-4 h-4 text-cyan-400"></i> Clinical Treatment Protocol & Prescriptions
                        </h3>
                        <span class="text-[10px] font-mono text-cyan-300 bg-cyan-950 px-2.5 py-1 rounded border border-cyan-800">
                            Aquaculture Pharmacopeia Regimen
                        </span>
                    </div>

                    <div id="treatmentBlank" class="py-8 text-center text-xs text-slate-500 font-mono">
                        Treatment regimens and clinical medication notes will appear upon confirmed diagnosis.
                    </div>

                    <div id="treatmentContent" class="hidden flex-col gap-4">
                        
                        <!-- Pathology Overview -->
                        <div class="bg-dark-900/80 p-4 rounded-xl border border-white/5">
                            <span class="text-[10px] font-mono uppercase text-slate-400 block mb-1">Pathological Etiology & Clinical Symptoms</span>
                            <p id="medEtiology" class="text-xs text-slate-200 leading-relaxed font-sans">--</p>
                        </div>

                        <!-- 4 Structured Clinical Cards -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                            
                            <!-- Card 1: Active Pharmaceutical Agents -->
                            <div class="bg-dark-900/80 p-4 rounded-xl border border-white/5 flex flex-col gap-1">
                                <div class="flex items-center gap-1.5 text-cyan-400 text-xs font-bold font-mono">
                                    <i data-lucide="shield-alert" class="w-4 h-4"></i> Active Drug / Chemotherapeutic
                                </div>
                                <div id="medDrug" class="text-xs font-semibold text-white mt-1">--</div>
                                <div id="medDrugClass" class="text-[10px] text-slate-400 font-mono mt-0.5">--</div>
                            </div>

                            <!-- Card 2: Immersion / Oral Administration -->
                            <div class="bg-dark-900/80 p-4 rounded-xl border border-white/5 flex flex-col gap-1">
                                <div class="flex items-center gap-1.5 text-emerald-400 text-xs font-bold font-mono">
                                    <i data-lucide="beaker" class="w-4 h-4"></i> Dosage Concentration & Course
                                </div>
                                <div id="medDose" class="text-xs text-slate-200 mt-1 leading-normal">--</div>
                            </div>

                            <!-- Card 3: Biosecurity & Pond Sanitation -->
                            <div class="bg-dark-900/80 p-4 rounded-xl border border-white/5 flex flex-col gap-1">
                                <div class="flex items-center gap-1.5 text-yellow-400 text-xs font-bold font-mono">
                                    <i data-lucide="waves" class="w-4 h-4"></i> Environmental & Water Quality Protocol
                                </div>
                                <div id="medBio" class="text-xs text-slate-200 mt-1 leading-normal">--</div>
                            </div>

                            <!-- Card 4: Contraindications -->
                            <div class="bg-dark-900/80 p-4 rounded-xl border border-white/5 flex flex-col gap-1">
                                <div class="flex items-center gap-1.5 text-rose-400 text-xs font-bold font-mono">
                                    <i data-lucide="alert-octagon" class="w-4 h-4"></i> Precautions & Contraindications
                                </div>
                                <div id="medCaution" class="text-xs text-slate-200 mt-1 leading-normal">--</div>
                            </div>

                        </div>
                    </div>
                </div>

            </div>

        </div>
    </main>

    <!-- Client Script -->
    <script>
        lucide.createIcons();

        const API_URL = "https://aquascan-backend-hqko.onrender.com/predict";

        // Comprehensive Veterinary Pharmacopeia Database
        const PHARMACOPEIA = {
            'Bacterial gill disease': {
                severity: 'CRITICAL SEVERITY',
                color: 'red',
                etiology: 'Epizootic condition predominantly caused by Flavobacterium branchiophilum. Microscopic evaluation indicates branchial epithelial hyperplasia, severe mucus hyper-secretion, clubbed lamellae, and subsequent asphyxiation.',
                drug: 'Chloramine-T / Benzalkonium Chloride',
                drugClass: 'Quaternary Ammonium / Oxidizing Halogen',
                dose: 'Chloramine-T short bath at 10-15 mg/L for 60 min under continuous active aeration. Repeat every alternate day for 3 pulses. Alternatively, Benzalkonium chloride flush at 2 mg/L for 30 min.',
                bio: 'Drastically reduce feeding; suspend inorganic fertilization; ensure dissolved oxygen exceeds 6.0 mg/L. Flush pond bottom with 25% freshwater.',
                caution: 'Never administer Chloramine-T in acidic water (pH < 6.5) or extremely soft water, as toxicity is significantly heightened.'
            },
            'Bacterial Red disease': {
                severity: 'HIGH SEVERITY',
                color: 'red',
                etiology: 'Manifests as hemorrhagic septicemia, external petechial hemorrhages along the ventral belly, ascites, and scale protrusion caused by mixed opportunistic bacterial vectors.',
                drug: 'Oxytetracycline HCl / Enrofloxacin',
                drugClass: 'Broad-Spectrum Tetracycline / Fluoroquinolone',
                dose: '55-75 mg/kg fish biomass in medicated pellets daily for 10 continuous days. For non-feeding broodstock, administer immersion dip at 25-30 mg/L for 60 min.',
                bio: 'Immediate quarantine of visibly ulcerated stock. Sanitize dry earthen pond dykes using Quicklime (Calcium Oxide) at 200-250 kg/ha.',
                caution: 'Adhere strictly to a 21-day withdrawal period prior to harvest for commercial human consumption.'
            },
            'Bacterial diseases - Aeromoniasis': {
                severity: 'HIGH SEVERITY',
                color: 'amber',
                etiology: 'Acute to chronic infection triggered by Aeromonas hydrophila complex. Presents deep dermal ulcerations, necrotic musculature exposure, abdominal distention, and exophthalmia.',
                drug: 'Florfenicol / Potassium Permanganate (KMnO4)',
                drugClass: 'Synthetic Fluorinated Amphenicol / Oxidizer',
                dose: 'Florfenicol blended in feed at 10 mg/kg biomass daily for 10 days. Pre-treat culture tanks with KMnO4 at 2.0-3.0 mg/L static bath for 2 hours.',
                bio: 'Dredge bottom decomposing organic silt. Keep unionized ammonia below 0.02 mg/L and nitrites under 0.1 mg/L.',
                caution: 'Potassium permanganate rapidly consumes dissolved oxygen; emergency aeration must remain active throughout treatment.'
            },
            'Fungal diseases - Saprolegniasis': {
                severity: 'MODERATE SEVERITY',
                color: 'amber',
                etiology: 'Oomycete infection characterized by filamentous, cotton-wool-like mycelial tufts anchoring on pre-existing lesions, abrasions, or unfertilized fish eggs.',
                drug: 'Formalin (37% w/v) / Sodium Chloride (NaCl)',
                drugClass: 'Aldehyde Anti-Parasitic / Electrolyte Osmoregulator',
                dose: 'Industrial Formalin immersion dip at 150-250 mg/L for 30-45 min. Or hyper-saline immersion bath (NaCl at 20-25 g/L for 15-20 min).',
                bio: 'Remove dead specimens and decomposing vegetation. Avoid rough handling during grading to eliminate mucosal scratches.',
                caution: 'Do not use Formalin at water temperatures below 10°C or above 25°C without active supplemental oxygenation.'
            },
            'Parasitic diseases': {
                severity: 'MODERATE SEVERITY',
                color: 'amber',
                etiology: 'Ectoparasitic proliferation of ciliates or monogeneans (Trichodina, Ichthyophthirius, Dactylogyrus) inducing gill erosion, flashing, and mucus sloughing.',
                drug: 'Trichlorfon (Dipterex) / Copper Sulphate (CuSO4)',
                drugClass: 'Organophosphate Acetylcholinesterase Inhibitor / Heavy Metal Salt',
                dose: 'Trichlorfon bath applied at 0.25-0.50 mg/L active substance. Alternatively, CuSO4 calculated according to water alkalinity: Total Alkalinity (mg/L) / 100 = CuSO4 (mg/L).',
                bio: 'Vacuum and siphon pond bottom mulm. Quarantine incoming fingerlings for 14 days prior to stocking.',
                caution: 'Organophosphates are toxic to invertebrates and scaleless fish; do not use in pangasius or shrimp polycultures.'
            },
            'Viral diseases': {
                severity: 'CRITICAL LOCKDOWN',
                color: 'rose',
                etiology: 'Systemic viremia causing petechial gill pallor, hepatic necrosis, and sudden acute mortality across juvenile stocks. No chemotherapy is curative.',
                drug: 'Povidone Iodine (PVP-I) / Virucidal Disinfectants',
                drugClass: 'Topical Iodophor / Bio-decontaminant',
                dose: 'PVP-I immersion at 50-100 mg/L for equipment sterilization. Disinfect hatchery holding tanks with active Chlorine (200 mg/L).',
                bio: 'Immediate biosecurity lockdown: humanely cull heavily infected stock, incinerate mortalities, and drain ponds for 21 days under direct sun.',
                caution: 'Never discharge wastewater from viral-infected tanks into communal rivers or adjoining fish farming waterways.'
            },
            'Healthy Fish': {
                severity: 'NORMAL / OPTIMAL',
                color: 'emerald',
                etiology: 'Intact epithelial tissue, uniform pigmentation, clear branchial filaments, and absence of necrotic lesion targets or fungal hyphae.',
                drug: 'Immunostimulants & Aquatic Probiotics',
                drugClass: 'Nutritional Biological Supplement',
                dose: 'Feed-grade Beta-glucan (0.1% of feed ration) paired with Ascorbic Acid (Vitamin C at 500 mg/kg feed) daily.',
                bio: 'Maintain water chemical parameters: pH 7.2-7.8, Dissolved Oxygen > 5.5 mg/L, and Unionized Ammonia < 0.01 mg/L.',
                caution: 'Avoid overfeeding and maintain bi-weekly microbiological water sampling.'
            }
        };

        const specimenInput = document.getElementById('specimenInput');
        const dropZone = document.getElementById('dropZone');
        const dropContent = document.getElementById('dropContent');
        const specimenBadge = document.getElementById('specimenBadge');
        const origViewer = document.getElementById('origViewer');
        const origBlank = document.getElementById('origBlank');
        const origResolution = document.getElementById('origResolution');
        const camViewer = document.getElementById('camViewer');
        const camBlank = document.getElementById('camBlank');
        const diagnoseBtn = document.getElementById('diagnoseBtn');
        const latencyTimer = document.getElementById('latencyTimer');
        const diagCard = document.getElementById('diagCard');
        const diagnosisTitle = document.getElementById('diagnosisTitle');
        const diagnosisScore = document.getElementById('diagnosisScore');
        const severityBadge = document.getElementById('severityBadge');
        const probBarContainer = document.getElementById('probBarContainer');
        const treatmentBlank = document.getElementById('treatmentBlank');
        const treatmentContent = document.getElementById('treatmentContent');
        const medEtiology = document.getElementById('medEtiology');
        const medDrug = document.getElementById('medDrug');
        const medDrugClass = document.getElementById('medDrugClass');
        const medDose = document.getElementById('medDose');
        const medBio = document.getElementById('medBio');
        const medCaution = document.getElementById('medCaution');

        let stagedFile = null;

        specimenInput.addEventListener('change', function(e) {
            if (e.target.files && e.target.files[0]) {
                processFile(e.target.files[0]);
            }
        });

        ['dragenter', 'dragover'].forEach(name => {
            dropZone.addEventListener(name, (e) => {
                e.preventDefault();
                dropZone.classList.add('border-cyan-400', 'bg-cyan-950/20');
            });
        });

        ['dragleave', 'drop'].forEach(name => {
            dropZone.addEventListener(name, (e) => {
                e.preventDefault();
                dropZone.classList.remove('border-cyan-400', 'bg-cyan-950/20');
            });
        });

        dropZone.addEventListener('drop', (e) => {
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                processFile(e.dataTransfer.files[0]);
            }
        });

        function processFile(file) {
            stagedFile = file;
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    origResolution.innerText = `${img.naturalWidth} × ${img.naturalHeight} px`;
                };
                img.src = e.target.result;

                origViewer.src = e.target.result;
                origViewer.classList.remove('hidden');
                origBlank.classList.add('hidden');

                camViewer.classList.add('hidden');
                camBlank.classList.remove('hidden');

                specimenBadge.innerText = file.name;
                specimenBadge.className = "text-[10px] font-mono text-cyan-400 uppercase font-bold";

                dropContent.innerHTML = `
                    <div class="w-10 h-10 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
                        <i data-lucide="check" class="w-5 h-5"></i>
                    </div>
                    <span class="text-xs font-semibold text-white">${file.name}</span>
                    <span class="text-[10px] text-cyan-400 font-mono">Ready for execution. Click button below.</span>
                `;
                lucide.createIcons();
                diagnoseBtn.disabled = false;
            };
            reader.readAsDataURL(file);
        }

        diagnoseBtn.addEventListener('click', async function() {
            if (!stagedFile) return;

            const startTime = performance.now();
            const formData = new FormData();
            formData.append("file", stagedFile);

            diagnoseBtn.disabled = true;
            diagnoseBtn.innerHTML = `
                <div class="spinner"></div>
                <span>Forward Propagating & Resolving Saliency...</span>
            `;

            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`Diagnostic server returned HTTP ${response.status}`);
                }

                const data = await response.json();
                const totalLatency = (performance.now() - startTime).toFixed(1);
                latencyTimer.innerText = `${totalLatency} ms`;

                // Display Grad-CAM
                camViewer.src = data.cam_image;
                camViewer.classList.remove('hidden');
                camBlank.classList.add('hidden');

                // Determine winner
                let topClass = data.primary_class || '';
                let topProb = 0;
                if (!topClass) {
                    for (const [cls, prob] of Object.entries(data.confidences)) {
                        if (prob > topProb) {
                            topProb = prob;
                            topClass = cls;
                        }
                    }
                } else {
                    topProb = data.confidences[topClass];
                }

                diagnosisTitle.innerText = topClass;
                diagnosisScore.innerText = `${(topProb * 100).toFixed(2)}%`;

                const protocol = PHARMACOPEIA[topClass] || PHARMACOPEIA['Healthy Fish'];

                // Update Severity Badge & Colors
                if (topClass === 'Healthy Fish') {
                    severityBadge.className = "px-2.5 py-0.5 rounded text-[10px] font-mono uppercase font-bold bg-emerald-950 text-emerald-300 border border-emerald-700";
                    diagnosisScore.className = "text-3xl font-extrabold font-mono text-emerald-400";
                } else if (protocol.severity.includes('CRITICAL')) {
                    severityBadge.className = "px-2.5 py-0.5 rounded text-[10px] font-mono uppercase font-bold bg-rose-950 text-rose-300 border border-rose-700 animate-pulse";
                    diagnosisScore.className = "text-3xl font-extrabold font-mono text-rose-400";
                } else {
                    severityBadge.className = "px-2.5 py-0.5 rounded text-[10px] font-mono uppercase font-bold bg-amber-950 text-amber-300 border border-amber-700";
                    diagnosisScore.className = "text-3xl font-extrabold font-mono text-amber-400";
                }
                severityBadge.innerText = protocol.severity;

                // Render Probability Bars
                probBarContainer.innerHTML = '';
                const sorted = Object.entries(data.confidences).sort((a, b) => b[1] - a[1]);
                sorted.forEach(([clsName, score]) => {
                    const pct = (score * 100).toFixed(1);
                    const row = document.createElement('div');
                    row.className = "flex flex-col gap-1 font-mono text-xs";
                    const isWinner = clsName === topClass;
                    row.innerHTML = `
                        <div class="flex justify-between ${isWinner ? 'text-white font-bold' : 'text-slate-400'}">
                            <span>${clsName}</span>
                            <span class="${isWinner ? 'text-cyan-300' : 'text-slate-400'}">${pct}%</span>
                        </div>
                        <div class="h-1.5 w-full bg-dark-900 rounded-full overflow-hidden border border-white/5">
                            <div class="h-full ${isWinner ? 'bg-cyan-400' : 'bg-slate-600'} rounded-full transition-all duration-700" style="width: ${pct}%"></div>
                        </div>
                    `;
                    probBarContainer.appendChild(row);
                });

                // Render Structured Pharmacopeia
                treatmentBlank.classList.add('hidden');
                treatmentContent.classList.remove('hidden');
                treatmentContent.classList.add('flex');

                medEtiology.innerText = protocol.etiology;
                medDrug.innerText = protocol.drug;
                medDrugClass.innerText = protocol.drugClass;
                medDose.innerText = protocol.dose;
                medBio.innerText = protocol.bio;
                medCaution.innerText = protocol.caution;

            } catch (err) {
                alert("Diagnostic API Error: " + err.message + "\nPlease verify that the backend is active.");
            } finally {
                diagnoseBtn.disabled = false;
                diagnoseBtn.innerHTML = `
                    <i data-lucide="play" class="w-4 h-4 fill-current"></i>
                    <span>Execute Pathological Inference</span>
                `;
                lucide.createIcons();
            }
        });
    </script>
</body>
</html>
