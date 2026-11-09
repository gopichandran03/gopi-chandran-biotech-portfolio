# Content for the Moringa oleifera RNA-seq walkthrough.
# The interactive is a pipeline inspector showing the real commands and QC
# checkpoints for each stage - not fabricated expression data. Published
# figures for the public dataset are cited on the final slide.

PAGE = {
    "number": "06",
    "category": "Transcriptomics",
    "card_title": "Moringa oleifera RNA-seq profiling",
    "card_blurb": "A transcriptome workflow from reads to pathway annotation - with a stage-by-stage pipeline inspector showing the actual commands, the QC checkpoint at each step, and what failure looks like.",
    "cta": "Open pipeline inspector",
    "tags": ["RNA-seq", "HISAT2", "StringTie", "Annotation"],
    "meta": "Moringa oleifera transcriptome profiling for phytochemical biosynthesis genes: HISAT2, StringTie, TransDecoder, eggNOG-mapper, InterProScan and KEGG workflow with QC checkpoints at every stage.",
    "headline": "Reads are cheap.<br><em>Interpretation is the work.</em>",
    "sub": "Transcript profiling in Moringa oleifera to investigate genes associated with phytochemical biosynthesis - the drumstick tree whose leaves accumulate flavonoids, vitamins and micronutrients at unusual levels. This walkthrough is the workflow itself: every stage, the command that runs it, the quality checkpoint that decides whether to continue, and the failure mode that stage is there to catch.",
    "pills": [
        ("Linux workflow",),
        ("HISAT2 · StringTie · TransDecoder",),
        ("eggNOG-mapper · InterProScan · KEGG",),
        ("Public dataset", "solid"),
    ],
    "note": "<strong>Data provenance:</strong> this workflow was run against the publicly deposited <em>Moringa oleifera</em> RNA-seq dataset (NCBI BioProject <code>PRJNA394193</code>), not private or unpublished data. Assembly metrics I recorded for my own run are given on slide 3 alongside the published figures for the same dataset, so you can see both. The repository contains a runnable QC-summary script that operates on a clearly labelled example count matrix.",
    "footer_note": "Public dataset PRJNA394193 · workflow code in workflows/rnaseq/",
    "code": "workflows/rnaseq/README.md",
    "slides": [
        {
            "eyebrow": "01 · The organism",
            "title": "Why Moringa is worth sequencing",
            "body": """      <p class="lede">Moringa oleifera is a drought-tolerant tree whose leaves, seeds and pods are used as food, as a nutritional supplement and in traditional medicine across South Asia and sub-Saharan Africa. The interesting question for a transcriptomics project is <em>which genes</em> produce that chemistry, and <em>where in the plant</em> they act.</p>
      <div class="cols three">
        <div class="panel">
          <h3>Nutritional profile</h3>
          <p>Leaves accumulate vitamins and micronutrients, with iron and calcium of particular interest - which makes transporters and storage proteins as relevant as biosynthetic enzymes.</p>
        </div>
        <div class="panel">
          <h3>Secondary metabolites</h3>
          <p>Flavonoids including quercetin and kaempferol, plus phenylpropanoid and alkaloid pathway products - the compounds behind most of the medicinal claims.</p>
        </div>
        <div class="panel">
          <h3>Drought tolerance</h3>
          <p>A hardy tree in marginal conditions, so stress-response pathways are a second axis of interest alongside metabolism.</p>
        </div>
      </div>
      <h3 style="margin-top:26px">Why RNA-seq rather than genome sequencing</h3>
      <p>A genome tells you what the plant <em>could</em> make. A transcriptome across tissues tells you what each tissue is <em>actually</em> transcribing - which is the question when the practical interest is "are the valuable compounds made in the leaf, the seed or the flower?" Published work on this dataset sampled five tissues (leaf, root, stem, seed and flower) precisely to resolve that.</p>
      <div class="takeaway"><strong>Project framing:</strong> locate candidate genes for phytochemical biosynthesis and establish which tissue expresses them - a prerequisite for any downstream breeding, extraction or metabolic-engineering question.</div>""",
        },
        {
            "eyebrow": "02 · Interactive",
            "title": "The pipeline, stage by stage",
            "body": """      <p>Select any stage to see the command that runs it, what it consumes and produces, the checkpoint that decides whether to proceed, and what goes wrong if you skip the check. This is the workflow as actually operated, not a schematic.</p>

      <div class="demo viz">
        <div class="demo-head">
          <h3>RNA-seq workflow inspector</h3>
          <span class="tag">Real commands · public dataset</span>
        </div>
        <div class="demo-body">
          <div class="flow" id="stages" role="tablist" aria-label="Pipeline stages"></div>
          <div id="detail" style="margin-top:20px"></div>
        </div>
      </div>

      <div class="takeaway"><strong>The thing I would emphasise to anyone building their first pipeline:</strong> every stage above has a checkpoint, and the checkpoints are not optional decoration. A pipeline that runs end to end without error can still produce a confidently annotated transcriptome built on 40% rRNA contamination. The commands are the easy part.</div>""",
        },
        {
            "eyebrow": "03 · Metrics",
            "title": "Assembly metrics, mine and published",
            "body": """      <p>I want to put both sets of numbers side by side rather than quote only one, because the comparison is the useful thing.</p>
      <div class="tbl-scroll"><table>
        <thead><tr><th>Metric</th><th>My run</th><th>Published, same dataset</th><th>Comment</th></tr></thead>
        <tbody>
          <tr><td>Assembly size</td><td>79.79 Mb</td><td>—</td><td>Total assembled transcript sequence</td></tr>
          <tr><td>Transcript N50</td><td><strong>2,094 bp</strong></td><td><strong>2,094 bp</strong></td><td>Matches the published assembly for this dataset exactly</td></tr>
          <tr><td>Transcripts &gt; 200 bp</td><td>66,079</td><td>—</td><td>Before collapsing isoforms to gene models</td></tr>
          <tr><td>Reads assembled</td><td>—</td><td>271 million</td><td>Across five tissues</td></tr>
          <tr><td>Predicted gene models</td><td>—</td><td>17,148</td><td>Published pipeline combined the transcriptome with the <em>M. oleifera</em> genome</td></tr>
          <tr><td>Tissues</td><td colspan="2">Leaf, root, stem, seed, flower</td><td>Cultivar Bhagya (KDM-01)</td></tr>
        </tbody>
      </table></div>
      <div class="note neutral" style="margin-top:20px"><strong>On the N50 agreement:</strong> recovering the same N50 as the published assembly is a reassuring sign that the workflow was configured sensibly - it is a reproduction check, not an independent finding, and I present it as such. The gap between 66,079 transcripts and ~17,148 gene models is the ordinary and important difference between <em>transcripts</em> (isoforms, fragments) and <em>genes</em>; quoting the transcript count as a gene count would inflate the result roughly fourfold, and that conflation is one of the most common errors in transcriptome reporting.</div>
      <h3 style="margin-top:24px">What the published analysis found</h3>
      <ul>
        <li>Candidate genes for the biosynthesis of secondary metabolites, vitamins, and ion transporters were identified, with expression confirmed for selected leads by quantitative real-time PCR.</li>
        <li>Enzymes in the biosynthesis of vitamins and metabolites including <strong>quercetin and kaempferol</strong> were highly expressed in <strong>leaves, flowers and seeds</strong>.</li>
        <li><strong>Iron transporters and calcium storage proteins</strong> were expressed in <strong>root and leaves</strong>.</li>
        <li>Overall, leaves retained the highest amount of the small molecules of interest - supported by quantitative metabolite estimation and elemental analysis, not transcript data alone.</li>
      </ul>
      <div class="takeaway"><strong>Why that last point is the most important one:</strong> the transcript evidence and the chemistry agreed. Expression data alone would have been a hypothesis; the metabolite and elemental measurements are what turned it into a finding.</div>""",
        },
        {
            "eyebrow": "04 · Annotation",
            "title": "Turning sequences into biology",
            "body": """      <p>Assembly produces sequences. Annotation is what makes them mean something, and it works by stacking independent lines of evidence rather than trusting any single tool.</p>
      <div class="cols">
        <div class="panel">
          <h3>TransDecoder - find the coding regions</h3>
          <p>Identifies likely open reading frames within assembled transcripts. Without this, you are annotating untranslated regions and assembly artefacts alongside real proteins.</p>
        </div>
        <div class="panel">
          <h3>BLAST - homology to known proteins</h3>
          <p>The baseline evidence: what does this look like in a curated database? Strong, but inherits every error and bias in the reference.</p>
        </div>
        <div class="panel">
          <h3>InterProScan - domain architecture</h3>
          <p>Scans for protein domains and family signatures. Catches function that sequence similarity misses, because domain composition is often conserved where overall identity is not.</p>
        </div>
        <div class="panel">
          <h3>eggNOG-mapper - orthology-based transfer</h3>
          <p>Assigns function via orthologous groups, which is more principled than "best BLAST hit" because it reasons about evolutionary relationship rather than raw similarity.</p>
        </div>
      </div>
      <h3 style="margin-top:26px">KEGG: from genes to pathways</h3>
      <p>Mapping annotated genes onto KEGG pathways is what converts a gene list into a biological claim. For this project the pathways of interest were phenylpropanoid biosynthesis (the entry point to flavonoids), flavonoid biosynthesis itself, and the vitamin and micronutrient routes.</p>
      <div class="note"><strong>The interpretation trap:</strong> a pathway "present" in KEGG output can mean every enzyme in it was found, or that two enzymes out of fifteen were found and the rest inferred by the map's structure. Those are completely different claims. Before reporting a pathway as active I check enzyme-level coverage - how many distinct EC numbers in that pathway actually have transcript support - because the pathway diagram will happily draw arrows through steps you have no evidence for.</div>""",
        },
        {
            "eyebrow": "05 · Reproducibility",
            "title": "What makes a workflow re-runnable",
            "body": """      <p>The difference between a pipeline that works and a pipeline someone else can use is almost entirely bookkeeping - and the bookkeeping is where most bioinformatics projects quietly fail.</p>
      <div class="cols">
        <div class="panel lime">
          <h3>What I did</h3>
          <ul>
            <li>Shell scripts per stage with parameters at the top, not buried in command lines</li>
            <li>Tool versions recorded</li>
            <li>Intermediate outputs retained so a failed stage does not force a full re-run</li>
            <li>A QC report per stage rather than only at the end</li>
          </ul>
        </div>
        <div class="panel">
          <h3>What I would add now</h3>
          <ul>
            <li><strong>A workflow manager</strong> - Nextflow or Snakemake - so dependencies, resumption and parallelism are declared rather than hand-managed</li>
            <li><strong>Containers</strong> (Docker/Singularity) pinning exact tool versions; "HISAT2 2.2.1" in a README is not the same as a reproducible environment</li>
            <li><strong>A single config file</strong> for all paths and parameters</li>
            <li><strong>Checksums on inputs</strong>, so a silently changed reference is caught immediately</li>
            <li><strong>Automated MultiQC aggregation</strong> instead of reading per-sample reports by hand</li>
          </ul>
        </div>
      </div>
      <h3 style="margin-top:26px">The honest version of this project's reproducibility</h3>
      <p>It was reproducible by me, with my notes, on the same machine. That is the normal standard for student project work and it is not the standard I would want to meet in a professional setting - where "reproducible" has to mean a different person on different hardware gets the same numbers without asking me anything. Stating the gap is more useful than claiming the stronger version.</p>
      <div class="takeaway"><strong>Transferable lesson:</strong> the discipline that makes a bioinformatics pipeline trustworthy is the same discipline that makes a laboratory protocol trustworthy - parameters recorded, versions pinned, checkpoints documented, deviations noted. The medium changes; the habit does not.</div>""",
        },
        {
            "eyebrow": "06 · Code & sources",
            "title": "Run the QC summary, and where the numbers come from",
            "body": """      <p>The repository contains a small, honest piece of this workflow: a Python script that computes QC summaries over a count matrix and writes out tables and a plot. It is explicitly <em>not</em> the full HISAT2/StringTie pipeline - it operates on a labelled example count matrix so it runs anywhere in seconds.</p>
      <pre><code>python3 -m pip install -r requirements.txt
python3 workflows/rnaseq/qc_summary.py --counts workflows/rnaseq/data/example_counts.tsv --out qc/</code></pre>
      <p>It reports library sizes, detected-gene counts per sample, the distribution of counts per gene, the proportion of reads in the top expressed genes (a useful contamination signal), and sample-sample correlation. The README in that folder sets out what a full pipeline run would add.</p>
      <ul class="refs" style="margin-top:24px">
        <li><strong>Public dataset: 271 million reads assembled with an N50 of 2,094 bp across five tissues (leaf, root, stem, seed, flower) of <em>M. oleifera</em> cultivar Bhagya (KDM-01); data deposited as NCBI BioProject PRJNA394193</strong> - K. Mohamed Shafi et al., "Dataset for the combined transcriptome assembly of <em>M. oleifera</em> and functional annotation," <em>Data in Brief</em> 30:105416 (2020). <a href="https://doi.org/10.1016/j.dib.2020.105416" target="_blank" rel="noopener">doi:10.1016/j.dib.2020.105416</a>; <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7155000/" target="_blank" rel="noopener">PMC7155000</a>.</li>
        <li><strong>17,148 gene models predicted; candidate genes for secondary metabolites, vitamins and ion transporters, confirmed for selected leads by qRT-PCR; quercetin and kaempferol biosynthesis enzymes highly expressed in leaves, flowers and seeds; iron transporters and calcium storage proteins expressed in root and leaves; leaves retaining the highest amount of small molecules of interest, supported by metabolite quantification and elemental analysis</strong> - Ravooru, Rao, Sowdhamini et al., "The transcriptome enables the identification of candidate genes behind medicinal value of Drumstick tree (<em>Moringa oleifera</em>)," <em>Genomics</em> 112(1):621-628 (2020). <a href="https://doi.org/10.1016/j.ygeno.2019.04.014" target="_blank" rel="noopener">doi:10.1016/j.ygeno.2019.04.014</a>.</li>
        <li><strong>Phenylpropanoid, flavonoid and alkaloid pathway enzyme counts in <em>M. oleifera</em> seed transcriptome</strong> - M. D. K. Discar, "Transcriptomic approach to discover genes for secondary metabolite biosynthesis in <em>Moringa oleifera</em> Lam. seeds," MS thesis, Ateneo de Manila University (2017). <a href="https://archium.ateneo.edu/theses-dissertations/76" target="_blank" rel="noopener">Record</a>.</li>
        <li><strong>Tools:</strong> HISAT2 (Kim et al.), StringTie (Pertea et al.), TransDecoder (Haas et al.), eggNOG-mapper (Cantalapiedra et al.), InterProScan (Jones et al.), BLAST (Altschul et al.), KEGG (Kanehisa &amp; Goto).</li>
      </ul>
      <div class="note neutral"><strong>Attribution:</strong> the dataset and the published findings above are the work of the cited authors. My contribution is running and documenting the workflow against the public data, the assembly metrics reported for my own run on slide 3, and this walkthrough.</div>""",
        },
    ],
    "page_script": """<script>
(function(){
  'use strict';
  var STAGES=[
    {k:'qc', n:'1 · Raw read QC',
     cmd:'fastqc -t 8 -o qc/raw/ reads/*_1.fastq.gz reads/*_2.fastq.gz\\nmultiqc qc/raw/ -o qc/raw/',
     inp:'Paired-end FASTQ files, one pair per tissue',
     outp:'Per-sample HTML reports plus an aggregated MultiQC summary',
     check:'Per-base quality, adapter content, duplication level, GC distribution, overrepresented sequences.',
     fail:'A bimodal GC distribution usually means contamination; a spike in overrepresented sequences often means rRNA carry-over. Proceeding regardless produces an assembly whose most abundant "transcripts" are ribosomal RNA, and every downstream abundance estimate is distorted.'},
    {k:'trim', n:'2 · Trim & filter',
     cmd:'trimmomatic PE -threads 8 \\\\\\n  reads/S1_1.fastq.gz reads/S1_2.fastq.gz \\\\\\n  trim/S1_1P.fq.gz trim/S1_1U.fq.gz \\\\\\n  trim/S1_2P.fq.gz trim/S1_2U.fq.gz \\\\\\n  ILLUMINACLIP:adapters.fa:2:30:10 LEADING:3 TRAILING:3 \\\\\\n  SLIDINGWINDOW:4:20 MINLEN:36',
     inp:'Raw FASTQ plus the adapter sequences for the library kit actually used',
     outp:'Paired and unpaired trimmed reads',
     check:'Retention rate. Re-run FastQC on trimmed output and confirm adapter content has gone.',
     fail:'Over-trimming is as damaging as under-trimming - aggressive quality cutoffs shorten reads until they no longer map uniquely, which silently reduces mapping rate and biases against lower-quality but real transcripts. If retention drops below roughly 80% I investigate rather than accept it.'},
    {k:'align', n:'3 · Align (HISAT2)',
     cmd:'hisat2-build -p 8 genome.fa moringa_idx\\n\\nhisat2 -p 8 -x moringa_idx \\\\\\n  -1 trim/S1_1P.fq.gz -2 trim/S1_2P.fq.gz \\\\\\n  --dta --summary-file align/S1.summary \\\\\\n  | samtools sort -@ 4 -o align/S1.bam\\nsamtools index align/S1.bam',
     inp:'Trimmed reads and the reference genome',
     outp:'Coordinate-sorted, indexed BAM per sample',
     check:'Overall alignment rate, concordant pair rate, and the fraction of reads spanning splice junctions.',
     fail:'A low alignment rate with good read quality points at the wrong reference, residual contamination, or a genuinely divergent sample. The --dta flag matters here: it tailors the output for downstream transcript assembly, and omitting it degrades StringTie\\'s results in a way that is easy to miss.'},
    {k:'assemble', n:'4 · Assemble transcripts (StringTie)',
     cmd:'stringtie align/S1.bam -p 8 -G reference.gtf -o asm/S1.gtf -l S1\\n\\nstringtie --merge -G reference.gtf -o asm/merged.gtf asm/*.gtf\\n\\ngffcompare -r reference.gtf -o cmp asm/merged.gtf',
     inp:'Per-sample BAMs and, where available, a reference annotation',
     outp:'Per-sample GTFs, a merged assembly, and a comparison against the reference',
     check:'Transcript and gene counts, N50, exon-per-transcript distribution, and the gffcompare class codes showing how much is novel versus known.',
     fail:'Single-exon transcripts dominating the assembly usually indicates genomic DNA contamination or intronic noise rather than a biological discovery. A suspiciously high novel-transcript fraction is more often an assembly artefact than a finding.'},
    {k:'quant', n:'5 · Quantify',
     cmd:'stringtie align/S1.bam -e -B -p 8 -G asm/merged.gtf -o quant/S1/S1.gtf\\n\\nprepDE.py -i quant/ -g counts/gene_counts.csv -t counts/transcript_counts.csv',
     inp:'BAMs re-quantified against the merged assembly',
     outp:'Gene-level and transcript-level count matrices',
     check:'Library sizes within a comparable range; detected-gene counts consistent across samples; sample-sample correlation matching expected tissue relationships.',
     fail:'If one sample contributes a tiny library or correlates with nothing, it is a candidate for exclusion - and that decision must be made and recorded before any comparison, not after seeing which result you prefer.'},
    {k:'orf', n:'6 · Find coding regions',
     cmd:'TransDecoder.LongOrfs -t transcripts.fa\\nTransDecoder.Predict  -t transcripts.fa',
     inp:'Assembled transcript sequences',
     outp:'Predicted peptides, CDS and GFF3',
     check:'Proportion of transcripts with a complete ORF; peptide length distribution.',
     fail:'A low complete-ORF fraction suggests a fragmented assembly - annotating fragments produces partial domain hits that look like weak evidence for the wrong function.'},
    {k:'annot', n:'7 · Annotate function',
     cmd:'blastp -query peptides.faa -db swissprot \\\\\\n  -evalue 1e-5 -max_target_seqs 1 -outfmt 6 -num_threads 8 > blast.tsv\\n\\ninterproscan.sh -i peptides.faa -f TSV -goterms -pa -cpu 8\\n\\nemapper.py -i peptides.faa -o eggnog --cpu 8',
     inp:'Predicted peptides',
     outp:'Homology hits, domain assignments, GO terms, orthologous group assignments',
     check:'Annotation rate across all three methods, and crucially the agreement between them.',
     fail:'Taking the single best BLAST hit as the answer. Where homology, domain architecture and orthology disagree, that transcript needs a human decision, not an automatic label. Disagreement is information, and a pipeline that hides it produces a clean-looking annotation table nobody should trust.'},
    {k:'path', n:'8 · Pathway mapping',
     cmd:'# KEGG KAAS / KofamScan assignment, then enrichment\\nkofamscan -o kegg.txt peptides.faa\\n# summarise enzyme coverage per pathway of interest',
     inp:'Annotated genes with KO or EC assignments',
     outp:'Pathway assignments and enrichment results',
     check:'Enzyme-level coverage per pathway - how many distinct EC numbers in the pathway actually have transcript support.',
     fail:'Reporting a pathway as "present" on the strength of two enzymes out of fifteen. The KEGG map draws the whole pathway regardless of what you found, so the diagram implies evidence you do not have unless you report coverage explicitly.'}
  ];

  var bar=document.getElementById('stages'), det=document.getElementById('detail'), cur=0;

  function esc(s){return String(s).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}

  function paint(){
    bar.innerHTML='';
    STAGES.forEach(function(s,i){
      var b=document.createElement('button');
      b.className='flow-step';
      b.setAttribute('role','tab');
      b.setAttribute('aria-selected', i===cur?'true':'false');
      b.style.cssText='text-align:left;cursor:pointer;font:inherit;border:1px solid '+
        (i===cur?'var(--ink)':'var(--line)')+';background:'+(i===cur?'var(--green)':'var(--paper)');
      b.innerHTML='<b>'+esc(s.n.split(' · ')[0])+'</b><span>'+esc(s.n.split(' · ')[1])+'</span>';
      b.addEventListener('click',function(){ cur=i; paint(); });
      bar.appendChild(b);
    });
    var s=STAGES[cur];
    det.innerHTML=
      '<h3 style="margin:0 0 10px">'+esc(s.n)+'</h3>'+
      '<pre><code>'+esc(s.cmd)+'</code></pre>'+
      '<div class="cols" style="margin-top:14px">'+
        '<div class="panel"><h3>In</h3><p>'+esc(s.inp)+'</p>'+
          '<h3 style="margin-top:14px">Out</h3><p>'+esc(s.outp)+'</p></div>'+
        '<div class="panel blue"><h3>Checkpoint</h3><p>'+esc(s.check)+'</p></div>'+
      '</div>'+
      '<div class="note" style="max-width:none"><strong>What this check catches:</strong> '+esc(s.fail)+'</div>';
  }
  paint();
})();
</script>""",
}
