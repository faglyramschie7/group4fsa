import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');
const dataDir = path.join(rootDir, 'src', 'data');
const outFile = path.join(rootDir, 'public', 'llms.txt');

const deck = JSON.parse(
  fs.readFileSync(path.join(dataDir, 'presentation_deck.json'), 'utf8')
);
const assignments = JSON.parse(
  fs.readFileSync(path.join(dataDir, 'all_assignments_bundle.json'), 'utf8')
);

const lines = [];

lines.push('# GoTo Financial Statement Analysis (FSA) Study Master — Complete Presentation Deck');
lines.push('');
lines.push(
  '> Plain-text / Markdown version of the Group 4 Financial Statement Analysis presentation on **PT GoTo Gojek Tokopedia Tbk (IDX: GOTO)**, generated for AI assistants (Gemini, ChatGPT, Claude) and study use from `src/data/presentation_deck.json`.'
);
lines.push('');
lines.push('- **Live App:** https://group4fsa.crosswing.app/');
lines.push('- **AI-Readable Deck:** https://group4fsa.crosswing.app/llms.txt');
lines.push('- **Company:** PT GoTo Gojek Tokopedia Tbk (IDX: GOTO)');
lines.push('- **Valuation Date:** December 30, 2025 | **Market Price:** Rp 25.00 / share');
lines.push('- **Final Recommendation:** **SELL GOTO at Rp 25.00**');
lines.push('');
lines.push('---');
lines.push('');

for (const slide of deck) {
  const slideLabel = slide.is_appendix
    ? `Appendix Slide ${slide.slide_num}`
    : `Slide ${slide.slide_num}`;

  lines.push(`## ${slideLabel}: ${slide.title}`);
  if (slide.subtitle) {
    lines.push(`**${slide.subtitle}**`);
  }

  const meta = [
    slide.section_tag ? `Section: ${slide.section_tag}` : null,
    slide.time_budget ? `Time Budget: ${slide.time_budget}` : null,
    slide.rubric_points ? `Rubric: ${slide.rubric_points}` : null,
  ].filter(Boolean);
  if (meta.length) {
    lines.push(`*${meta.join(' | ')}*`);
  }
  lines.push('');

  if (Array.isArray(slide.kpis) && slide.kpis.length > 0) {
    lines.push('### Key Metrics & KPIs');
    for (const kpi of slide.kpis) {
      const sub = kpi.sub ? ` (${kpi.sub})` : '';
      lines.push(`- **${kpi.label}:** \`${kpi.val}\`${sub}`);
      if (kpi.detail_explanation) {
        lines.push(`  - Explanation: ${kpi.detail_explanation}`);
      }
      if (kpi.formula) {
        lines.push(`  - Formula: \`${kpi.formula}\``);
      }
      if (Array.isArray(kpi.calc_steps) && kpi.calc_steps.length > 0) {
        lines.push('  - Calculation Steps:');
        for (const step of kpi.calc_steps) {
          lines.push(`    - ${step}`);
        }
      }
      if (kpi.data_origin) {
        lines.push(`  - Source: ${kpi.data_origin}`);
      }
    }
    lines.push('');
  }

  if (slide.table && Array.isArray(slide.table.headers) && Array.isArray(slide.table.rows)) {
    lines.push(`### ${slide.table.title || 'Data Table'}`);
    lines.push('');
    lines.push(`| ${slide.table.headers.join(' | ')} |`);
    lines.push(`| ${slide.table.headers.map(() => '---').join(' | ')} |`);
    for (const row of slide.table.rows) {
      const cells = row.map((cell) => String(cell ?? '').replace(/\|/g, '\\|').replace(/\n/g, ' '));
      lines.push(`| ${cells.join(' | ')} |`);
    }
    lines.push('');
  }

  if (Array.isArray(slide.cards) && slide.cards.length > 0) {
    lines.push('### Key Takeaways & Analysis');
    for (const card of slide.cards) {
      if (card.title) {
        lines.push(`#### ${card.title}`);
      }
      if (Array.isArray(card.bullets)) {
        for (const b of card.bullets) {
          const prefix = b.bold ? `**${b.bold}** ` : '';
          lines.push(`- ${prefix}${b.text || ''}`);
        }
      }
      if (card.detail_explanation) {
        lines.push(`- *Context:* ${card.detail_explanation}`);
      }
      lines.push('');
    }
  }

  if (slide.speaker_notes) {
    lines.push('### Speaker Notes');
    lines.push(slide.speaker_notes);
    lines.push('');
  }

  if (slide.source_footer) {
    lines.push(`*Sources: ${slide.source_footer}*`);
    lines.push('');
  }

  lines.push('---');
  lines.push('');
}

if (Array.isArray(assignments) && assignments.length > 0) {
  lines.push('## Supporting Coursework & Assignments Index');
  lines.push('');
  for (const item of assignments) {
    lines.push(`- **${item.code || item.id} (${item.week || 'Coursework'}): ${item.title}**`);
    if (item.summary) {
      lines.push(`  - ${item.summary}`);
    }
  }
  lines.push('');
}

fs.writeFileSync(outFile, `${lines.join('\n').trimEnd()}\n`, 'utf8');
const stats = fs.statSync(outFile);
console.log(`Generated ${outFile} (${(stats.size / 1024).toFixed(1)} KB, ${deck.length} slides)`);
