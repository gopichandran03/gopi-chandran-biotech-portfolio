# Content for the HTB-182 cell culture operations walkthrough.
#
# The calculator on slide 3 computes from the user's own counts using standard
# vessel geometry and the line's published doubling time. It reports no
# experimental results. Cell line characteristics and handling parameters are
# from ATCC and cited; caffeine pharmacology is from the primary literature
# and cited.

PAGE = {
    "number": "03",
    "category": "Cell culture operations",
    "card_title": "HTB-182 culture operations",
    "home_title": "HTB-182 continuous culture &amp; caffeine treatment",
    "card_blurb": "Continuous maintenance of a lung squamous carcinoma line, caffeine treatment design, scaling up and down, cryopreservation and what to do when the incubator fails - with a culture planning calculator.",
    "cta": "Open culture calculator",
    "demo_label": "Open the culture calculator",
    "tags": ["Mammalian cell culture", "Aseptic technique", "Cryopreservation", "Experimental design"],
    "meta": "Continuous maintenance of HTB-182 (NCI-H520) lung squamous carcinoma cells: passaging, caffeine treatment design, scale up and down, cryopreservation, emergency preparedness, and a culture planning calculator.",
    "headline": "A cell line is a culture you keep alive<br><em>on a schedule you don't control.</em>",
    "sub": "Continuous maintenance of HTB-182 at UMBC - a human lung squamous cell carcinoma line - alongside caffeine treatment work, scaling the culture up and down as experiments demand, cryopreservation, and the preparedness that decides whether an incubator failure costs you a weekend or costs you the line. This is the operational discipline that every result downstream rests on.",
    "pills": [
        ("UMBC · laboratory", "solid"),
        ("HTB-182 / NCI-H520",),
        ("BSL-1 · adherent",),
        ("Planning calculator", "accent"),
    ],
    "note": "<strong>Scope:</strong> this walkthrough covers culture operations and experimental design - the handling, planning and contingency work I do. Cell line characteristics and handling parameters are from ATCC's published product information and are cited on the final slide; caffeine pharmacology is from the primary literature and cited. The calculator computes from <em>your</em> numbers using standard vessel geometry; it reports no experimental results of mine, and specific protocol parameters in use at UMBC are not reproduced here.",
    "footer_note": "ATCC handling parameters and caffeine pharmacology cited on the final slide",
    "slides": [
        {
            "eyebrow": "01 · The line",
            "title": "What HTB-182 is, and why it matters to the work",
            "body": """      <p class="lede">HTB-182 is the ATCC designation for NCI-H520, a human lung squamous cell carcinoma line derived in 1982 by A. F. Gazdar and colleagues from a lung mass taken from a patient with squamous cell carcinoma of the lung.</p>
      <div class="cols">
        <div class="panel">
          <h3>Characteristics</h3>
          <ul>
            <li><strong>Organism:</strong> <em>Homo sapiens</em>, male</li>
            <li><strong>Tissue / disease:</strong> lung, squamous cell carcinoma</li>
            <li><strong>Morphology:</strong> epithelial</li>
            <li><strong>Growth:</strong> adherent</li>
            <li><strong>Biosafety level:</strong> 1</li>
            <li><strong>Cellosaurus:</strong> CVCL_1566</li>
            <li>Stains positive for keratin and vimentin, negative for neurofilament triplet protein</li>
            <li>Clones in soft agar with or without serum; tumorigenic in nude mice</li>
          </ul>
        </div>
        <div class="panel blue">
          <h3>Handling parameters</h3>
          <ul>
            <li><strong>Medium:</strong> ATCC-formulated RPMI-1640 (30-2001) + 10% FBS</li>
            <li><strong>Incubation:</strong> 37 °C, 5% CO<sub>2</sub>, humidified</li>
            <li><strong>Dissociation:</strong> 0.25% trypsin / 0.03% EDTA</li>
            <li><strong>Subcultivation ratio:</strong> 1:3 to 1:6</li>
            <li><strong>Medium renewal:</strong> 2-3 times per week</li>
            <li><strong>Doubling time:</strong> 61 h in medium with serum; 25-32 h serum-free</li>
            <li><strong>Cryopreservation:</strong> complete growth medium + 5% DMSO</li>
            <li><strong>Storage:</strong> vapour phase of liquid nitrogen - <strong>not</strong> -70 °C</li>
          </ul>
        </div>
      </div>
      <div class="note neutral" style="margin-top:20px"><strong>The characteristic that shapes the biology:</strong> HTB-182 expresses <strong>greatly reduced levels of p53 mRNA</strong> relative to normal lung tissue, while showing no gross structural DNA abnormalities. Slide 4 is why that matters when you put a DNA-damage-checkpoint drug on these cells: a line with compromised p53 leans harder on the checkpoints that do not run through p53.</div>
      <div class="takeaway"><strong>Why a 61-hour doubling time is an operational fact, not a footnote:</strong> it is slow. A line that doubles in 24 hours forgives a missed day; this one does not recover a lost week quickly, and every plan on the following slides is built backwards from it.</div>""",
        },
        {
            "eyebrow": "02 · Maintenance",
            "title": "What continuous maintenance actually looks like",
            "body": """      <p>"Maintaining a cell line" sounds like a background task. It is a standing commitment with a fixed rhythm that does not pause for exams, holidays or anyone's schedule.</p>
      <div class="flow">
        <div class="flow-step"><b>Daily</b><span>Visual check - confluence, morphology, medium colour, any sign of contamination</span></div>
        <div class="flow-step"><b>2-3× weekly</b><span>Medium renewal</span></div>
        <div class="flow-step"><b>At confluence</b><span>Passage - wash, trypsinise, neutralise, count, reseed at 1:3 to 1:6</span></div>
        <div class="flow-step"><b>Every passage</b><span>Record passage number, split ratio, count, viability, observations</span></div>
        <div class="flow-step"><b>Periodically</b><span>Freeze down vials; refresh the working bank; mycoplasma check</span></div>
      </div>
      <h3 style="margin-top:26px">The judgements that are not in the protocol</h3>
      <div class="cols">
        <div class="panel">
          <h3>Reading the flask before you touch it</h3>
          <p>Medium colour is a pH readout: yellowing means acidification from metabolism, and on a slow-growing line that usually means it is overdue rather than overgrown. Cloudiness that was not there yesterday is the one observation that should stop everything.</p>
        </div>
        <div class="panel">
          <h3>Confluence is an estimate, not a measurement</h3>
          <p>"About 80%" is a trained eye on a microscope. Getting consistent is why the same person passaging a line week after week produces more reproducible downstream data than a rota of people each doing it correctly.</p>
        </div>
        <div class="panel">
          <h3>Trypsinisation has a window</h3>
          <p>Under-trypsinise and you leave cells and skew the count; over-trypsinise and you damage membranes and lose viability. On an adherent epithelial line you watch for rounding and gentle tapping rather than running a timer.</p>
        </div>
        <div class="panel">
          <h3>Passage number is a real variable</h3>
          <p>Lines drift. Growth rate, morphology and drug response can all shift at high passage. Recording passage number is what lets you ask later whether an odd result came from the biology or from the cells having been in culture too long.</p>
        </div>
      </div>
      <div class="takeaway"><strong>The link to the quality project in this portfolio:</strong> consistency here <em>is</em> process control. Every control chart in project 02 assumes the measurement was collected the same way each time - and in cell culture, that assumption is a person's technique.</div>""",
        },
        {
            "eyebrow": "03 · Interactive",
            "title": "Plan a passage, an experiment, or a freeze",
            "body": """      <p>Three calculations I actually do at the bench, with the geometry and the line's published doubling time built in. Enter your own counts.</p>

      <div class="demo viz">
        <div class="demo-head">
          <h3>HTB-182 culture planning calculator</h3>
          <span class="tag">Your counts · standard vessel geometry</span>
        </div>
        <div class="demo-body">
          <div class="controls" style="margin-bottom:18px">
            <label class="control">Calculation
              <select id="mode">
                <option value="split">Passage &amp; split</option>
                <option value="plan">Plan backwards from an experiment</option>
                <option value="freeze">Cryopreservation / cell bank</option>
              </select>
            </label>
            <label class="control">Doubling time (h)
              <input type="number" id="dt" min="12" max="120" step="1" value="61" style="width:100px">
            </label>
          </div>

          <div id="fields" class="controls"></div>
          <div class="readout" id="results"></div>
          <div id="extra" style="margin-top:16px"></div>

          <figure>
            <svg id="cc-chart" viewBox="0 0 740 250" role="img" aria-labelledby="cc-t">
              <title id="cc-t">Projected cell number over time after seeding</title>
            </svg>
            <figcaption id="cc-cap"></figcaption>
          </figure>
          <div class="legend">
            <span><i style="background:var(--series-1)"></i>Projected cell number</span>
            <span><i style="background:var(--series-2)"></i>Target or confluence threshold</span>
          </div>
        </div>
      </div>

      <div class="note" style="margin-top:20px"><strong>What the projection assumes:</strong> unconstrained exponential growth at a fixed doubling time, no lag phase after seeding, and 100% plating efficiency. Real cultures have a lag of a day or so after passage, slow as they approach confluence, and plate at less than 100%. So treat the curve as an <em>upper bound</em> on how fast you will get there, and build a day of slack into any plan that has a deadline attached.</div>""",
        },
        {
            "eyebrow": "04 · Caffeine",
            "title": "Treating with caffeine - what it does and how to design it",
            "body": """      <p>Caffeine is a useful laboratory tool rather than a dietary curiosity, and the reason is specific: it inhibits the kinases that run the DNA damage response.</p>
      <div class="cols">
        <div class="panel">
          <h3>The mechanism</h3>
          <p>Caffeine inhibits the catalytic activity of <strong>ATM</strong> and the related kinase <strong>ATR</strong>, at concentrations similar to those that cause radiosensitization. Downstream, it blocks ATM-dependent activation of Chk2 and prevents the Cdc25C serine-216 phosphorylation that holds the G2/M checkpoint - abrogating the checkpoint and letting damaged cells proceed into mitosis.</p>
          <p style="margin-top:10px">Reported in-vitro IC<sub>50</sub> values: approximately <strong>1 mM for ATM</strong> and <strong>3 mM for ATR</strong>, with inhibition of ATM-mediated Chk2 Thr68 phosphorylation around 200 µM. DNA-PKcs is resistant; Chk1 is only marginally suppressed.</p>
        </div>
        <div class="panel sand">
          <h3>Why HTB-182 is an interesting background for it</h3>
          <p>This line expresses greatly reduced p53. Caffeine reverses the S and G2 checkpoint responses to ionising radiation and the ATR/Chk1-dependent S checkpoint after UVC, while having <strong>little effect on the G1 checkpoint</strong> - which is the p53-dependent one.</p>
          <p style="margin-top:10px">So in a p53-compromised line, you are removing checkpoint capacity from a cell that already has less of it. That is the experimentally interesting part, and it is also the reason results here will not transfer cleanly to a p53-wild-type line.</p>
        </div>
      </div>
      <h3 style="margin-top:26px">Design points I would insist on</h3>
      <ul>
        <li><strong>Vehicle control, always.</strong> Caffeine is typically dissolved in medium or a small volume of solvent; the control gets the identical volume of whatever the stock was made in.</li>
        <li><strong>Prepare stock fresh and filter-sterilise.</strong> Caffeine stocks are made at high concentration and diluted into medium; sterility and accurate dilution both matter more than they look.</li>
        <li><strong>Pre-treat before the insult.</strong> Published checkpoint work commonly adds caffeine to the medium around 30 minutes before irradiation and keeps it present for the duration.</li>
        <li><strong>Plan a dose-response, not a single dose.</strong> The ATM and ATR IC<sub>50</sub> values differ roughly three-fold, so a single concentration cannot distinguish which kinase you are acting on.</li>
        <li><strong>Watch the exposure duration.</strong> With prolonged exposure caffeine has been reported to <em>induce</em> a DNA damage response itself, rather than only suppressing one - so a long incubation is a different experiment from a short one.</li>
        <li><strong>Seed density affects everything.</strong> Confluent cultures respond differently from subconfluent ones; the calculator on slide 3 exists partly so treatment-day density is a planned number rather than whatever the flask happened to reach.</li>
      </ul>
      <div class="note neutral" style="margin-top:20px"><strong>Two caveats worth stating plainly.</strong> First, caffeine is <strong>not a specific ATM/ATR inhibitor</strong> - it acts on other enzymes including cyclic AMP phosphodiesterase, and it has been shown to induce an ATM- and p53-independent G1 delay by a mechanism that is still not established. Any result attributed to "ATM inhibition" on caffeine evidence alone is over-interpreted. Second, the millimolar concentrations used in these experiments are one to two orders of magnitude above the plasma concentrations reached by ordinary coffee consumption. This is a pharmacological tool at a laboratory dose; nothing here says anything about drinking coffee.</div>""",
        },
        {
            "eyebrow": "05 · Scaling",
            "title": "Scaling up and down without wasting the line",
            "body": """      <p>Experiments arrive in different sizes. The culture has to be grown to meet them and then brought back down, and on a 61-hour doubling time both directions have to be planned a week ahead.</p>
      <div class="tbl-scroll"><table>
        <thead><tr><th>Vessel</th><th>Growth area</th><th>Typical working volume</th><th>Typical use</th></tr></thead>
        <tbody>
          <tr><td>96-well plate (per well)</td><td>0.32 cm²</td><td>0.1-0.2 mL</td><td>Viability and dose-response screens</td></tr>
          <tr><td>24-well plate (per well)</td><td>1.9 cm²</td><td>0.5-1 mL</td><td>Small treatment arms</td></tr>
          <tr><td>12-well plate (per well)</td><td>3.8 cm²</td><td>1-2 mL</td><td>Imaging, small lysates</td></tr>
          <tr><td>6-well plate (per well)</td><td>9.6 cm²</td><td>2-3 mL</td><td>Treatment arms for protein or RNA</td></tr>
          <tr><td>T25 flask</td><td>25 cm²</td><td>5-7 mL</td><td>Routine maintenance; recovery after thaw</td></tr>
          <tr><td>T75 flask</td><td>75 cm²</td><td>10-15 mL</td><td>Standard working flask; expansion</td></tr>
          <tr><td>T175 flask</td><td>175 cm²</td><td>25-35 mL</td><td>Bulk expansion ahead of a freeze or a large experiment</td></tr>
        </tbody>
      </table></div>
      <div class="cols" style="margin-top:22px">
        <div class="panel lime">
          <h3>Scaling up</h3>
          <p>Work backwards from the experiment: cells needed → seeding density → vessels → how many doublings from today's flask → start date. On this line that arithmetic usually says "start a week earlier than feels necessary", which is precisely why it is worth doing on paper rather than by instinct.</p>
          <p style="margin-top:10px">Split across more vessels at the same seeding density rather than overloading one - a flask seeded too densely reaches confluence before the experiment and has to be passaged again, which resets the clock.</p>
        </div>
        <div class="panel">
          <h3>Scaling down</h3>
          <p>After a large experiment you do not want to keep feeding three T175s. Drop back to a single maintenance flask, and - importantly - <strong>bank the surplus rather than discarding it</strong>. An expansion that has already been grown is the cheapest cryopreservation opportunity you will get.</p>
          <p style="margin-top:10px">Scaling down is also when passage number creeps up unnoticed, because a maintenance flask passaged on autopilot accumulates passages with nothing to show for them. Thaw a fresh low-passage vial instead of carrying one culture indefinitely.</p>
        </div>
      </div>
      <div class="takeaway"><strong>The planning habit:</strong> a culture should always be sized to a known forward commitment. Flasks maintained with no experiment behind them burn reagent, incubator space and passage number - three resources that are all genuinely finite.</div>""",
        },
        {
            "eyebrow": "06 · Cryopreservation",
            "title": "The cell bank is the insurance policy",
            "body": """      <p>Everything above assumes the culture survives. Cryopreservation is the only thing that makes that assumption safe, and a bank is only as good as the discipline behind it.</p>
      <div class="cols">
        <div class="panel">
          <h3>Freezing</h3>
          <ul>
            <li>Harvest in <strong>log phase</strong>, not at confluence - healthy, actively dividing cells survive freezing best</li>
            <li>Freeze medium: complete growth medium with <strong>5% DMSO</strong> for this line per ATCC</li>
            <li>DMSO is cytotoxic at room temperature: resuspend and get to the freezing container promptly</li>
            <li>Controlled cooling at roughly <strong>-1 °C per minute</strong> to -80 °C, then transfer to liquid nitrogen</li>
            <li>Label every vial: line, passage number, date, cells per vial, operator</li>
          </ul>
        </div>
        <div class="panel blue">
          <h3>Storing</h3>
          <ul>
            <li><strong>Vapour phase</strong> of liquid nitrogen, not submerged - ATCC recommends vapour phase unless necessary otherwise</li>
            <li><strong>Never -70 °C for long-term storage</strong> - it results in loss of viability</li>
            <li>Maintain an inventory map: tank, rack, box, position</li>
            <li>Split the bank across <strong>two locations</strong> if at all possible - one tank failure should not be an extinction event</li>
          </ul>
        </div>
      </div>
      <h3 style="margin-top:26px">Master and working banks</h3>
      <p>The structure that makes a line survivable long-term: freeze a <strong>master bank</strong> at the lowest passage you can, touch it rarely, and use it only to generate a <strong>working bank</strong> at a slightly higher passage. Routine thaws come from the working bank. When the working bank runs low, go back to the master once and regenerate.</p>
      <p>The payoff is that every experiment over years starts from material a known, small number of passages from the original - rather than from a culture that has been continuously passaged and has quietly drifted.</p>
      <div class="takeaway"><strong>Thawing matters as much as freezing:</strong> thaw rapidly at 37 °C, dilute out of DMSO promptly, and check viability. ATCC's procedure for this line transfers the vial contents into 9 mL of complete medium and centrifuges at approximately 125 × g for 5-10 minutes. A vial thawed carelessly can fail and will look like a bad freeze from three years ago.</div>""",
        },
        {
            "eyebrow": "07 · Emergency",
            "title": "When something fails at 2 a.m.",
            "body": """      <p class="lede">Preparedness in cell culture is not a policy document. It is a set of decisions made in advance, because the ones made in the moment are made by whoever happens to be there.</p>
      <div class="tbl-scroll"><table>
        <thead><tr><th>Failure</th><th>What it costs</th><th>Prepared response</th></tr></thead>
        <tbody>
          <tr><td><strong>Incubator CO<sub>2</sub> failure</strong></td><td>pH rises; cultures stressed or lost within hours</td><td>Alarm with out-of-hours contact; a validated second incubator with space kept free; move cultures and record the excursion</td></tr>
          <tr><td><strong>Incubator temperature failure</strong></td><td>Depends on direction - overheating is fast and fatal</td><td>Same: alarm, relocate, document. Do not return cultures to an incubator that has not been re-qualified</td></tr>
          <tr><td><strong>Power outage</strong></td><td>Incubators, freezers and the LN<sub>2</sub> monitor all at once</td><td>Know what is on emergency power before it happens; keep freezer doors shut; LN<sub>2</sub> tanks hold passively but the level alarm may not</td></tr>
          <tr><td><strong>Liquid nitrogen level low</strong></td><td>Potentially the entire bank</td><td>Level alarm plus a scheduled manual check; a standing fill contract; the second-location bank is the real mitigation</td></tr>
          <tr><td><strong>Bacterial or fungal contamination</strong></td><td>One culture, or every culture in the incubator</td><td>Discard - do not attempt to rescue a working culture with antibiotics; decontaminate the incubator and biosafety cabinet; thaw fresh from the bank; investigate the source before resuming</td></tr>
          <tr><td><strong>Mycoplasma</strong></td><td>Invisible, invalidates past results</td><td>Routine testing is the only detection; quarantine new or incoming lines; if positive, discard and restart from a tested vial</td></tr>
          <tr><td><strong>Key person unavailable</strong></td><td>A line maintained by one person stops</td><td>Written protocol, current inventory, a second trained person, and a schedule that someone else can read</td></tr>
        </tbody>
      </table></div>
      <div class="cols" style="margin-top:22px">
        <div class="panel lime">
          <h3>The questions worth answering before you need them</h3>
          <ul>
            <li>If this incubator failed tonight, where would the cultures go?</li>
            <li>If every flask were lost tomorrow, how many vials are banked, at what passage, and where?</li>
            <li>Who gets the alarm, and can they physically get in?</li>
            <li>If I were unavailable for two weeks, could someone else maintain this line from what is written down?</li>
          </ul>
        </div>
        <div class="panel">
          <h3>Why contamination gets discarded</h3>
          <p>Rescuing a contaminated working culture with antibiotics is tempting and almost always wrong: it selects resistant organisms, can mask rather than clear the problem, and leaves every downstream result questionable. The bank exists precisely so that discarding is the cheap option.</p>
        </div>
      </div>
      <div class="takeaway"><strong>The underlying point:</strong> the most valuable thing in the incubator is not the cells - they are replaceable from a vial. It is the <em>continuity</em>: a line at a known passage with an unbroken record. That is what preparedness protects, and it is what a portfolio claim of "cell culture experience" should actually mean.</div>""",
        },
        {
            "eyebrow": "08 · Sources",
            "title": "References",
            "body": """      <ul class="refs">
        <li><strong>HTB-182 / NCI-H520 cell line characteristics and handling: human lung squamous cell carcinoma, male, epithelial, adherent, biosafety level 1; derived in 1982 by A. F. Gazdar from a lung mass; greatly reduced p53 mRNA relative to normal lung tissue with no gross structural DNA abnormalities; keratin and vimentin positive, neurofilament triplet protein negative; clones in soft agar with or without serum; ATCC-formulated RPMI-1640 (30-2001) with 10% FBS; 37 °C, 5% CO<sub>2</sub>; 0.25% trypsin / 0.03% EDTA; subcultivation ratio 1:3 to 1:6; medium renewal 2-3 times per week; doubling time 61 h with serum and 25-32 h serum-free; cryopreservation in complete growth medium with 5% DMSO; storage in the vapour phase of liquid nitrogen rather than submerged, and not at -70 °C; thaw into 9.0 mL complete medium and centrifuge at approximately 125 × g for 5-10 minutes</strong> - ATCC product information, <a href="https://www.atcc.org/products/htb-182" target="_blank" rel="noopener">HTB-182 (NCI-H520 [H520])</a>. Cellosaurus accession <a href="https://www.cellosaurus.org/CVCL_1566" target="_blank" rel="noopener">CVCL_1566</a>.</li>
        <li><strong>Caffeine inhibits the catalytic activity of ATM and ATR at concentrations similar to those causing radiosensitization; DNA-PKcs resistant; Chk1 only marginally suppressed; caffeine-treated A549 lung carcinoma cells irradiated in G2 fail to arrest progression into mitosis</strong> - Sarkaria, Busby, Tibbetts, Roos, Taya, Karnitz &amp; Abraham, "Inhibition of ATM and ATR kinase activities by the radiosensitizing agent, caffeine," <em>Cancer Research</em> 59(17):4375-4382 (1999). <a href="https://pubmed.ncbi.nlm.nih.gov/10485486/" target="_blank" rel="noopener">PMID 10485486</a>.</li>
        <li><strong>2 mM caffeine abrogating the G2/M checkpoint by inhibiting ATM, preventing Chk2 activation and Cdc25C serine-216 phosphorylation; inhibition of ATM-mediated Chk2 Thr68 phosphorylation with an IC<sub>50</sub> of approximately 200 µM</strong> - Zhou, Chaturvedi, Spring, Scott, Johanson, Mishra, Mattern, Winkler &amp; Khanna, "Caffeine abolishes the mammalian G2/M DNA damage checkpoint by inhibiting ataxia-telangiectasia-mutated kinase activity," <em>Journal of Biological Chemistry</em> 275(14):10342-10348 (2000). <a href="https://doi.org/10.1074/jbc.275.14.10342" target="_blank" rel="noopener">doi:10.1074/jbc.275.14.10342</a>.</li>
        <li><strong>In-vitro IC<sub>50</sub> of approximately 1 mM for ATM and approximately 3 mM for ATR; caffeine reversing S and G2 checkpoint responses to ionising radiation and the ATR/Chk1-dependent S checkpoint response to UVC with little effect on G1; caffeine inducing an ATM- and p53-independent G1 delay saturating at 2 mM; caffeine not being a specific ATM/ATR inhibitor, with activity on other enzymes including cyclic AMP phosphodiesterase; caffeine added 30 minutes prior to irradiation and maintained for the experiment</strong> - "Caffeine and human DNA metabolism: the magic and the mystery," <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4046582" target="_blank" rel="noopener">PMC4046582</a>.</li>
        <li><strong>Prolonged caffeine exposure inducing a DNA damage response and p53 activation rather than only suppressing one, with cells stalling at G2/M</strong> - Baker laboratory, preprint, <a href="https://www.biorxiv.org/content/biorxiv/early/2016/08/29/072058.full.pdf" target="_blank" rel="noopener">bioRxiv 072058</a>.</li>
        <li><strong>Alternative published handling parameters for NCI-H520 (doubling time 32-60 h; split ratio 1:3 to 1:4; complete medium with 10% DMSO as an alternative freeze medium; storage at approximately -150 to -196 °C)</strong> - Cytion product data sheet, <a href="https://www.cytion.com/us/NCI-H520-Cells/305063" target="_blank" rel="noopener">NCI-H520 Cells (305063)</a>. Included because suppliers differ on these values and the difference is worth knowing.</li>
      </ul>
      <div class="note neutral"><strong>Attribution:</strong> the cell line was derived and characterised by other researchers, and the caffeine pharmacology above is the work of the cited authors. My contribution is the culture operations - maintenance, treatment setup, scaling, banking - the planning calculator on slide 3, and this walkthrough. Protocol parameters specific to the UMBC laboratory are not reproduced here.</div>""",
        },
    ],
    "page_script": """<script>
(function(){
  'use strict';
  var VESSELS=[
    {n:'96-well (per well)', a:0.32,  v:0.15},
    {n:'24-well (per well)', a:1.9,   v:0.75},
    {n:'12-well (per well)', a:3.8,   v:1.5},
    {n:'6-well (per well)',  a:9.6,   v:2.5},
    {n:'T25 flask',          a:25,    v:6},
    {n:'T75 flask',          a:75,    v:12},
    {n:'T175 flask',         a:175,   v:30}
  ];
  // A workable confluent density for an adherent epithelial monolayer.
  // Adjustable because it is a property of the line and the operator's eye.
  var CONFLUENT_PER_CM2 = 1.0e5;

  var mode=document.getElementById('mode'), dt=document.getElementById('dt');
  var fields=document.getElementById('fields'), results=document.getElementById('results'),
      extra=document.getElementById('extra');
  var svg=document.getElementById('cc-chart'), cap=document.getElementById('cc-cap');
  var NS='http://www.w3.org/2000/svg';
  var store={};

  function esc(s){return String(s).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
  function mk(t,a,x){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);if(x!==undefined)e.textContent=x;return e}
  function num(v){return Number(v).toLocaleString(undefined,{maximumFractionDigits:0})}
  function sci(v){
    if(v>=1e6) return (v/1e6).toFixed(2)+' \\u00d7 10\\u2076';
    if(v>=1e3) return (v/1e3).toFixed(1)+' \\u00d7 10\\u00b3';
    return num(v);
  }
  function vesselOptions(sel){
    return VESSELS.map(function(v,i){
      return '<option value="'+i+'"'+(i===sel?' selected':'')+'>'+v.n+'</option>';
    }).join('');
  }

  var FIELDS={
    split:[
      {id:'from', label:'Harvested from', type:'vessel', def:5},
      {id:'count',label:'Viable cells counted (total)', type:'number', def:6000000, step:100000},
      {id:'to',   label:'Reseed into', type:'vessel', def:5},
      {id:'ratio',label:'Split ratio 1:N', type:'number', def:4, min:2, max:12, step:1}
    ],
    plan:[
      {id:'need', label:'Cells needed on the day', type:'number', def:12000000, step:500000},
      {id:'to',   label:'Experiment vessel', type:'vessel', def:3},
      {id:'wells',label:'Number of wells / vessels', type:'number', def:24, min:1, step:1},
      {id:'have', label:'Cells you have today', type:'number', def:3000000, step:100000}
    ],
    freeze:[
      {id:'count', label:'Viable cells available', type:'number', def:20000000, step:1000000},
      {id:'per',   label:'Cells per vial', type:'number', def:3000000, step:500000},
      {id:'dmso',  label:'DMSO in freeze medium (%)', type:'number', def:5, min:5, max:10, step:1},
      {id:'master',label:'Reserve as master bank (vials)', type:'number', def:3, min:0, step:1}
    ]
  };

  function buildFields(){
    var f=FIELDS[mode.value];
    fields.innerHTML=f.map(function(x){
      if(x.type==='vessel'){
        return '<label class="control">'+esc(x.label)+
          '<select id="f-'+x.id+'">'+vesselOptions(store[x.id]!==undefined?store[x.id]:x.def)+'</select></label>';
      }
      var v = store[x.id]!==undefined ? store[x.id] : x.def;
      return '<label class="control">'+esc(x.label)+
        '<input type="number" id="f-'+x.id+'" value="'+v+'"'+
        (x.min!==undefined?' min="'+x.min+'"':'')+(x.max!==undefined?' max="'+x.max+'"':'')+
        (x.step?' step="'+x.step+'"':'')+' style="width:150px"></label>';
    }).join('');
    f.forEach(function(x){
      var el=document.getElementById('f-'+x.id);
      el.addEventListener('input',function(){ store[x.id]=+el.value; compute(); });
      el.addEventListener('change',function(){ store[x.id]=+el.value; compute(); });
      store[x.id] = +el.value;
    });
  }

  function tile(v,label,cls){
    return '<div><b'+(cls?' class="'+cls+'"':'')+'>'+v+'</b><small>'+esc(label)+'</small></div>';
  }

  function compute(){
    var td=Math.max(1,+dt.value||61);
    var m=mode.value, proj=null;

    if(m==='split'){
      var from=VESSELS[store.from], to=VESSELS[store.to];
      var count=Math.max(0,store.count||0), ratio=Math.max(2,store.ratio||2);
      var seed=count/ratio;
      var density=seed/to.a;
      var confluentAt=CONFLUENT_PER_CM2*to.a;
      var doublings = seed>0 ? Math.log2(confluentAt/seed) : 0;
      var days = doublings>0 ? doublings*td/24 : 0;
      results.innerHTML =
        tile(sci(seed),'Cells seeded per vessel')+
        tile(num(Math.round(density)),'Seeding density /cm\\u00b2')+
        tile(ratio,'Vessels from this harvest')+
        tile(days>0?days.toFixed(1)+' d':'already confluent','Projected to confluence', days<2?'flag':'ok')+
        tile(to.v+' mL','Working volume per vessel');
      extra.innerHTML='<p style="font-size:.88rem;color:var(--text-secondary);margin:0">'+
        'Harvested from <strong>'+esc(from.n)+'</strong> ('+from.a+' cm\\u00b2) into <strong>'+esc(to.n)+
        '</strong> ('+to.a+' cm\\u00b2). ATCC gives a subcultivation ratio of 1:3 to 1:6 for this line'+
        (ratio>6?' \\u2014 <strong>1:'+ratio+' is beyond that range</strong>, so expect a long lag or poor recovery.':
         (ratio<3?' \\u2014 <strong>1:'+ratio+' is tighter than that range</strong>; the flask will be confluent again quickly.':'.'))+
        '</p>';
      proj={start:seed, target:confluentAt, targetLabel:'confluent', td:td};
      cap.textContent='Projected growth from the seeding density above to a confluent monolayer, '+
        'assuming unconstrained exponential growth at the doubling time set above.';

    } else if(m==='plan'){
      var to2=VESSELS[store.to];
      var wells=Math.max(1,store.wells||1);
      var perWell=Math.max(0,store.need||0)/wells;
      var totalNeed=Math.max(0,store.need||0);
      var have=Math.max(1,store.have||1);
      var doublings2=Math.log2(totalNeed/have);
      var days2=doublings2>0?doublings2*td/24:0;
      var density2=perWell/to2.a;
      var medium=(to2.v*wells);
      results.innerHTML=
        tile(sci(perWell),'Cells per '+to2.n.replace(' (per well)',''))+
        tile(num(Math.round(density2)),'Seeding density /cm\\u00b2')+
        tile(doublings2>0?doublings2.toFixed(1):'0','Doublings required')+
        tile(days2>0?Math.ceil(days2)+' d':'ready now','Start this many days ahead', days2>10?'flag':'ok')+
        tile(medium.toFixed(0)+' mL','Medium needed to seed');
      extra.innerHTML='<p style="font-size:.88rem;color:var(--text-secondary);margin:0">'+
        'Add a day of slack for the post-passage lag, and a margin for plating efficiency below 100% \\u2014 '+
        'so plan on <strong>'+(Math.ceil(days2)+2)+' days</strong> rather than '+Math.ceil(days2)+
        '. At '+td+' h per doubling, every extra doubling costs '+(td/24).toFixed(1)+' days.</p>';
      proj={start:have, target:totalNeed, targetLabel:'target', td:td};
      cap.textContent='Projected growth from the cells you have today to the number the experiment needs. '+
        'The marker line is the target; where the curve crosses it is the earliest the experiment can run.';

    } else {
      var cnt=Math.max(0,store.count||0), per=Math.max(1,store.per||1);
      var vials=Math.floor(cnt/per);
      var master=Math.min(vials,Math.max(0,store.master||0));
      var working=vials-master;
      var freezeVol=vials*1.0;
      results.innerHTML=
        tile(vials,'Vials at this density')+
        tile(master,'Master bank vials')+
        tile(working,'Working bank vials', working<2?'flag':'ok')+
        tile(store.dmso+'%','DMSO in freeze medium')+
        tile(freezeVol.toFixed(0)+' mL','Freeze medium needed (1 mL/vial)');
      extra.innerHTML='<p style="font-size:.88rem;color:var(--text-secondary);margin:0">'+
        'ATCC specifies complete growth medium with <strong>5% DMSO</strong> for this line; some suppliers use 10%. '+
        'Cool at about -1 \\u00b0C per minute to -80 \\u00b0C, then transfer to the vapour phase of liquid nitrogen \\u2014 '+
        'not -70 \\u00b0C, which loses viability. '+
        (working<2?'<strong>Fewer than two working vials is not a bank</strong> \\u2014 expand further before freezing.':
                   'Split the bank across two storage locations if you can.')+
        '</p>';
      proj=null;
      cap.textContent='No growth projection for a freeze \\u2014 the chart shows the recovery curve for one thawed vial '+
        'seeded into a T25, which is the number that matters when you come back to the bank.';
      var thawStart=per*0.7; // allow for post-thaw viability loss
      proj={start:thawStart, target:CONFLUENT_PER_CM2*25, targetLabel:'confluent (T25)', td:td};
    }

    draw(proj);
  }

  function draw(p){
    while(svg.childNodes.length>1) svg.removeChild(svg.lastChild);
    if(!p||!(p.start>0)){ svg.appendChild(mk('text',{x:20,y:30,'class':'axis-label'},'Enter a cell count to project growth.')); return; }
    var W=740,H=250,L=76,R=96,T=28,B=42;
    var maxDays=Math.max(4, Math.min(21, Math.ceil(Math.log2(Math.max(p.target,p.start*2)/p.start)*p.td/24)+2));
    var vals=[];
    for(var d=0;d<=maxDays;d+=0.25) vals.push([d, p.start*Math.pow(2, d*24/p.td)]);
    var top=Math.max(p.target, vals[vals.length-1][1]);
    var lo=Math.log10(Math.max(1,p.start*0.6)), hi=Math.log10(top*1.25);
    var sx=function(d){return L+d/maxDays*(W-L-R)};
    var sy=function(v){return T+(hi-Math.log10(Math.max(1,v)))/(hi-lo)*(H-T-B)};

    for(var e=Math.ceil(lo);e<=Math.floor(hi);e++){
      var v=Math.pow(10,e);
      svg.appendChild(mk('line',{x1:L,x2:W-R,y1:sy(v),y2:sy(v),'class':'grid-line'}));
      svg.appendChild(mk('text',{x:L-9,y:sy(v)+4,'class':'axis-label','text-anchor':'end'},'10'+String(e).replace(/\\d/g,function(c){return '\\u2070\\u00b9\\u00b2\\u00b3\\u2074\\u2075\\u2076\\u2077\\u2078\\u2079'[+c]})));
    }
    svg.appendChild(mk('line',{x1:L,x2:W-R,y1:H-B,y2:H-B,'class':'axis-line'}));
    var step=maxDays<=7?1:(maxDays<=14?2:3);
    for(var d2=0;d2<=maxDays;d2+=step){
      svg.appendChild(mk('text',{x:sx(d2),y:H-22,'class':'axis-label','text-anchor':'middle'},d2));
    }
    svg.appendChild(mk('text',{x:(L+W-R)/2,y:H-5,'class':'axis-title','text-anchor':'middle'},'Days after seeding'));
    svg.appendChild(mk('text',{x:L-62,y:T-12,'class':'axis-title'},'Cells (log)'));

    svg.appendChild(mk('line',{x1:L,x2:W-R,y1:sy(p.target),y2:sy(p.target),
      stroke:'var(--series-2)','stroke-width':2,'stroke-dasharray':'5 4'}));
    svg.appendChild(mk('text',{x:W-R+6,y:sy(p.target)+4,'class':'axis-label',fill:'var(--series-2)'},p.targetLabel));

    var dpath=vals.map(function(pt,i){return (i?'L':'M')+sx(pt[0]).toFixed(1)+' '+sy(pt[1]).toFixed(1)}).join(' ');
    svg.appendChild(mk('path',{d:dpath,'class':'series-line',stroke:'var(--series-1)'}));

    var cross=null;
    for(var i=0;i<vals.length;i++){ if(vals[i][1]>=p.target){ cross=vals[i][0]; break; } }
    if(cross!==null){
      svg.appendChild(mk('circle',{cx:sx(cross),cy:sy(p.target),r:5,fill:'var(--series-1)',
        stroke:'var(--surface-1)','stroke-width':2}));
      svg.appendChild(mk('text',{x:sx(cross),y:sy(p.target)-12,'class':'value-label','text-anchor':'middle'},
        'day '+cross.toFixed(1)));
    }
  }

  mode.addEventListener('change',function(){ store={}; buildFields(); compute(); });
  dt.addEventListener('input',compute);
  buildFields(); compute();
})();
</script>""",
}
