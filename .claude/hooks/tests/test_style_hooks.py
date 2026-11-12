"""Offline tests for the style hooks: per-turn pulse, chat markers, reply checker.

Workspace-agnostic: the same file runs in every workspace that carries the hooks.
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOOKS = ROOT / '.claude' / 'hooks'
BANNER = 'CHAT MARKERS —'


class StyleHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.env = dict(os.environ, CLAUDE_PROJECT_DIR=str(ROOT), TMPDIR=self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_hook(self, command, **payload):
        payload.setdefault('session_id', 'style-test')
        result = subprocess.run(command, input=json.dumps(payload), text=True,
                                capture_output=True, env=self.env, cwd=self.temp.name)
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout

    def prompt(self, text):
        return self.run_hook(['bash', str(HOOKS / 'style-pulse.sh')], prompt=text)

    def check(self, event, **payload):
        return self.run_hook(['python3', str(HOOKS / 'check-style.py')],
                             hook_event_name=event, **payload)

    def test_pulse_every_turn_without_full_ruleset(self):
        for _ in range(12):
            text = self.prompt('continue')
            self.assertIn('LENGTH (enforce)', text)
            self.assertNotIn('# Response Style', text)
            self.assertNotIn('BROKEN', text)

    def test_dash_markers_fire_known_only(self):
        self.assertIn('`-how` — mechanism', self.prompt('Explain -how'))
        self.assertNotIn(BANNER, self.prompt('run ls -la, then re-check -- done'))

    def test_tilde_chat_marker_is_reported_unknown(self):
        text = self.prompt('old habit ~how')
        self.assertIn('UNKNOWN CHAT MARKER', text)
        self.assertNotIn('`-how` — mechanism', text)

    def test_pasted_fenced_and_quoted_markers_never_fire(self):
        for text in ['<pasted_content id="a">\n-how\n</pasted_content id="a">',
                     '```\n-how\n```\n> -how\nUse `-how` literally.']:
            with self.subTest(text=text):
                self.assertNotIn(BANNER, self.prompt(text))

    def test_long_reply_is_flagged_once(self):
        self.check('Stop', last_assistant_message='\n'.join('- line %d' % i for i in range(21)))
        verdict = self.check('UserPromptSubmit', prompt='continue')
        self.assertIn('reply length: 21 lines', verdict)
        self.assertNotIn('STYLE CHECK', self.check('UserPromptSubmit', prompt='continue'))

    def test_short_reply_without_plan_passes(self):
        self.check('Stop', last_assistant_message='- One.\n- Two.\n- Three.\n- Four.\n- Five.')
        self.assertNotIn('STYLE CHECK', self.check('UserPromptSubmit', prompt='continue'))

    def test_prose_and_sixteen_word_bullet_are_flagged(self):
        reply = 'A short prose answer.\n- ' + ' '.join(['word'] * 16)
        self.check('Stop', last_assistant_message=reply)
        verdict = self.check('UserPromptSubmit', prompt='continue')
        self.assertIn('chat text outside bullets', verdict)
        self.assertIn('bullet cap 15 words', verdict)

    def test_opening_queue_passes_with_long_counter_line(self):
        reply = ('### Queue\n\n'
                 '- 5 / 15 from ui re-design · 2 open · open: which breakpoint owns the overflow\n'
                 '- 7 / 17 (+2) from models renaming\n\n---\n\n- Verdict.\n- Which breakpoint owns it?')
        self.check('Stop', last_assistant_message=reply)
        self.assertNotIn('STYLE CHECK', self.check('UserPromptSubmit', prompt='continue'))

    def test_queue_then_plan_then_rule_passes(self):
        reply = ('### Queue\n\n- 1 / 2 from ui\n\n### Plan\n\n- ✅ Audited rules\n- ✅ Ported hooks\n'
                 '- 🔄 Discuss the point\n- ⬜ Implement agreed changes\n\n---\n\n- Verdict.')
        self.check('Stop', last_assistant_message=reply)
        self.assertNotIn('STYLE CHECK', self.check('UserPromptSubmit', prompt='continue'))

    def test_queue_shape_is_flagged(self):
        cases = {'empty block': '### Queue\n\n---\n\n- Verdict.',
                 'not `{remaining}': '### Queue\n\n- ui re-design, five left\n\n---\n\n- Verdict.',
                 'pool at 0': '### Queue\n\n- 0 / 4 from models renaming\n\n---\n\n- Verdict.',
                 "not the reply's first block": '- Verdict.\n\n### Queue\n\n- 1 / 2 from ui',
                 'no `---` rule': '### Queue\n\n- 1 / 2 from ui\n\n### Notes\n\n- Verdict.'}
        for finding, reply in cases.items():
            with self.subTest(finding=finding):
                self.check('Stop', last_assistant_message=reply)
                self.assertIn(finding, self.check('UserPromptSubmit', prompt='continue'))


if __name__ == '__main__':
    unittest.main()
