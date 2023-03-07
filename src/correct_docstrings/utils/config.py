"""
Classes responsible for storing configuration for the script formatter.
"""
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from .docstring_filters import (
    DocstringFilterBase,
    EmptyLineBetweenDescriptionAndParams,
    NoRepeatedWhitespaces,
    ThirdPersonConverter,
    RemoveUnwantedPrefixes,
    EndOfSentencePunctuation,
    EnsureColonInParamDescription,
    IndentMultilineParamDescription,
    SentenceCapitalization,
    LineWrapping,
)


@dataclass
class DocstringFormatterConfig:
    """
    Configuration for the docstring formatter.
    """

    include_empty_line_between_description_and_params: bool = True
    include_no_repeated_whitespaces: bool = True
    include_remove_unwanted_prefixes: bool = True
    include_line_wrapper: bool = True
    include_third_person_converter: bool = False
    include_end_of_sentence_punctuation: bool = True
    include_ensure_colon_in_param_description: bool = True
    include_indent_multiline_param_description: bool = True
    include_sentence_capitalization: bool = True
    prefixes: Tuple[str] = tuple([":param", ":return", ":raises"])
    punctuation: str = "."
    indentation: str = " " * 2
    blocking_words: Tuple[str] = tuple(
        "not, to, a, an, the, for, in, of, and, or, as, if, but, nor, so, yet, at, by, "
        "from, into, like, over, after, before, between, into, through, with, without, "
        "during, without, until, up, upon, about, above, across, after, against, along, "
        "amid, among, anti, around, as, at, before, behind, below, beneath, beside, "
        "besides, between, beyond, concerning, considering, despite, down, during, "
        "except, excepting, excluding, following, for, from, in, inside, into, like, "
        "minus, near, of, off, on, onto, opposite, outside, over, past, per, plus, "
        "regarding, round, save, since, than, through, to, toward, towards, under, "
        "underneath, unlike, until, up, upon, versus, via, with, within, without".split(
            ", "
        )
    )
    modals: Tuple[str] = tuple(["can", "must", "should", "may", "might"])
    _verbs: Tuple[str] = tuple(
        "abide, accelerate, accept, accomplish, achieve, acquire, acted, activate, adapt, "
        "add, address, administer, admire, admit, adopt, advise, afford, agree, alert, "
        "alight, allow, altered, amuse, analyze, announce, annoy, answer, anticipate, "
        "apologize, appear, applaud, applied, appoint, appraise, appreciate, approve, "
        "arbitrate, argue, arise, arrange, arrest, arrive, ascertain, ask, assemble, "
        "assess, assist, assure, attach, attack, attain, attempt, attend, attract, "
        "audited, avoid, awake, back, bake, balance, ban, bang, bare, bat, bathe, "
        "battle, be, beam, bear, beat, become, beg, begin, behave, behold, belong, bend, "
        "beset, bet, bid, bind, bite, bleach, bleed, bless, blind, blink, blot, blow, blush, "
        "boast, boil, bolt, bomb, book, bore, borrow, bounce, bow, box, brake, branch, break, "
        "breathe, breed, brief, bring, broadcast, bruise, brush, bubble, budget, build, bump, "
        "burn, burst, bury, bust, buy, buze, calculate, call, can, camp, care, carry, carve, "
        "cast, catalog, catch, cause, challenge, change, charge, chart, chase, cheat, check, "
        "cheer, chew, choke, choose, chop, claim, clap, clarify, classify, clean, clear, "
        "cling, clip, close, clothe, coach, coil, collect, color, comb, come, command, "
        "communicate, compare, compete, compile, complain, complete, compose, compute, "
        "conceive, concentrate, conceptualize, concern, conclude, conduct, confess, confront, "
        "confuse, connect, conserve, consider, consist, consolidate, construct, consult, "
        "contain, continue, contract, control, convert, coordinate, copy, correct, correlate, "
        "cost, cough, counsel, count, cover, crack, crash, crawl, create, creep, critique, "
        "cross, crush, cry, cure, curl, curve, cut, cycle, dam, damage, dance, dare, deal, "
        "decay, deceive, decide, decorate, define, delay, delegate, delight, deliver, "
        "demonstrate, depend, describe, desert, deserve, design, destroy, detail, detect, "
        "determine, develop, devise, diagnose, dig, direct, disagree, disappear, disapprove, "
        "disarm, discover, dislike, dispense, display, disprove, dissect, distribute, dive, "
        "divert, divide, do, double, doubt, draft, drag, drain, dramatize, draw, dream, "
        "dress, drink, drip, drive, drop, drown, drum, dry, dust, dwell, earn, eat, edited, "
        "educate, eliminate, embarrass, employ, empty, enacted, encourage, end, endure, "
        "enforce, engineer, enhance, enjoy, enlist, ensure, enter, entertain, escape, "
        "establish, estimate, evaluate, examine, exceed, excite, excuse, execute, exercise, "
        "exhibit, exist, expand, expect, expedite, experiment, explain, explode, express, "
        "extend, extract, face, facilitate, fade, fail, fancy, fasten, fax, fear, feed, feel, "
        "fence, fetch, fight, file, fill, film, finalize, finance, find, fire, fit, fix, flap, "
        "flash, flee, fling, float, flood, flow, flower, fly, fold, follow, fool, forbid, force, "
        "forecast, forego, foresee, foretell, forget, forgive, form, formulate, forsake, frame, "
        "freeze, frighten, fry, gather, gaze, generate, get, give, glow, glue, go, govern, "
        "grab, graduate, grate, grease, greet, grin, grind, grip, groan, grow, guarantee, guard, "
        "guess, guide, hammer, hand, handle, handwrite, hang, happen, harass, harm, hate, haunt, "
        "head, heal, heap, hear, heat, help, hide, hit, hold, hook, hop, hope, hover, hug, hum, "
        "hunt, hurry, hurt, hypothesize, identify, ignore, illustrate, imagine, implement, "
        "impress, improve, improvise, include, increase, induce, influence, inform, initiate, "
        "inject, injure, inlay, innovate, input, inspect, inspire, install, institute, instruct, "
        "insure, integrate, intend, intensify, interest, interfere, interlay, interpret, "
        "interrupt, interview, introduce, invent, inventory, investigate, invite, irritate, itch, "
        "jail, jam, jog, join, joke, judge, juggle, jump, justify, keep, kept, kick, kill, kiss, "
        "kneel, knit, knock, knot, know, label, land, last, laugh, launch, lay, lead, lean, leap, "
        "learn, leave, lecture, led, lend, let, level, license, lick, lie, lifted, light, lighten, "
        "like, list, listen, live, load, locate, lock, log, long, look, lose, love, maintain, make, "
        "man, manage, manipulate, manufacture, map, march, mark, market, marry, match, mate, matter, "
        "mean, measure, meddle, mediate, meet, melt, melt, memorize, mend, mentor, milk, mine, "
        "mislead, miss, misspell, mistake, misunderstand, mix, moan, model, modify, monitor, moor, "
        "motivate, mourn, move, mow, muddle, mug, multiply, murder, nail, name, navigate, need, "
        "negotiate, nest, nod, nominate, normalize, note, notice, number, obey, object, observe, obtain, "
        "occur, offend, offer, officiate, open, operate, order, organize, oriented, originate, overcome, "
        "overdo, overdraw, overflow, overhear, overtake, overthrow, overwrite, owe, own, pack, paddle, "
        "paint, park, part, participate, pass, paste, pat, pause, pay, peck, pedal, peel, peep, perceive, "
        "perfect, perform, permit, persuade, phone, photograph, pick, pilot, pinch, pine, pinpoint, "
        "pioneer, place, plan, plant, play, plead, please, plug, point, poke, polish, pop, possess, post, "
        "pour, practice, praised, pray, preach, precede, predict, prefer, prepare, prescribe, present, "
        "preserve, preset, preside, press, pretend, prevent, prick, print, process, procure, produce, "
        "profess, program, progress, project, promise, promote, proofread, propose, protect, prove, "
        "provide, publicize, pull, pump, punch, puncture, punish, purchase, push, put, qualify, question, "
        "queue, quit, race, radiate, rain, raise, rank, rate, reach, read, realign, realize, reason, "
        "receive, recognize, recommend, reconcile, record, recruit, reduce, refer, reflect, refuse, regret, "
        "regulate, rehabilitate, reign, reinforce, reject, rejoice, relate, relax, release, rely, remain, "
        "remember, remind, remove, render, reorganize, repair, repeat, replace, reply, report, represent, "
        "reproduce, request, rescue, research, resolve, respond, restored, restructure, retire, retrieve, "
        "return, review, revise, rhyme, rid, ride, ring, rinse, rise, risk, rob, rock, roll, rot, rub, "
        "ruin, rule, run, rush, sack, sail, satisfy, save, saw, say, scare, scatter, schedule, scold, "
        "scorch, scrape, scratch, scream, screw, scribble, scrub, seal, search, secure, see, seek, select, "
        "sell, send, sense, separate, serve, service, set, settle, sew, shade, shake, shape, share, shave, "
        "shear, shed, shelter, shine, shiver, shock, shoe, shoot, shop, show, shrink, shrug, shut, sigh, "
        "sign, signal, simplify, sin, sing, sink, sip, sit, sketch, ski, skip, slap, slay, sleep, slide, "
        "sling, slink, slip, slit, slow, smash, smell, smile, smite, smoke, snatch, sneak, sneeze, sniff, "
        "snore, snow, soak, solve, soothe, soothsay, sort, sound, sow, spare, spark, sparkle, speak, "
        "specify, speed, spell, spend, spill, spin, spit, split, spoil, spot, spray, spread, spring, "
        "sprout, squash, squeak, squeal, squeeze, stain, stamp, stand, stare, start, stay, steal, steer, "
        "step, stick, stimulate, sting, stink, stir, stitch, stop, store, strap, streamline, strengthen, "
        "stretch, stride, strike, string, strip, strive, stroke, structure, study, stuff, sublet, subtract, "
        "succeed, suck, suffer, suggest, suit, summarize, supervise, supply, support, suppose, surprise, "
        "surround, suspect, suspend, swear, sweat, sweep, swell, swim, swing, switch, symbolize, synthesize, "
        "systemize, tabulate, take, talk, tame, tap, target, taste, teach, tear, tease, telephone, tell, "
        "tempt, terrify, test, thank, thaw, think, thrive, throw, thrust, tick, tickle, tie, time, tip, "
        "tire, touch, tour, tow, trace, trade, train, transcribe, transfer, transform, translate, transport, "
        "trap, travel, tread, treat, tremble, trick, trip, trot, trouble, troubleshoot, trust, try, tug, "
        "tumble, turn, tutor, twist, type, undergo, understand, undertake, undress, unfasten, unify, unite, "
        "unlock, unpack, untidy, update, upgrade, uphold, upset, use, utilize, vanish, verbalize, verify, "
        "vex, visit, wail, wait, wake, walk, wander, want, warm, warn, wash, waste, watch, water, wave, "
        "wear, weave, wed, weep, weigh, welcome, wend, wet, whine, whip, whirl, whisper, whistle, win, wind, "
        "wink, wipe, wish, withdraw, withhold, withstand, wobble, wonder, work, worry, wrap, wreck, wrestle, "
        "wriggle, wring, write, x-ray, yawn, yell, zip, zoom, validate".split(", ")
    )
    ignored_verbs: Tuple[str] = tuple([])

    @property
    def filters(self) -> List[DocstringFilterBase]:
        """
        Returns the selected filters.

        :return: List of selected filters.
        """

        _filters = []

        if self.include_line_wrapper:
            _filters.append(LineWrapping(self.prefixes), max_length=90)

        if self.include_empty_line_between_description_and_params:
            _filters.append(EmptyLineBetweenDescriptionAndParams(self.prefixes))

        if self.include_no_repeated_whitespaces:
            _filters.append(NoRepeatedWhitespaces(self.prefixes))

        if self.include_remove_unwanted_prefixes:
            _filters.append(RemoveUnwantedPrefixes(self.prefixes))

        if self.include_third_person_converter:
            _filters.append(
                ThirdPersonConverter(self.blocking_words, self.modals, self.verbs)
            )

        if self.include_end_of_sentence_punctuation:
            _filters.append(EndOfSentencePunctuation(self.punctuation))

        if self.include_ensure_colon_in_param_description:
            _filters.append(EnsureColonInParamDescription())

        if self.include_indent_multiline_param_description:
            _filters.append(IndentMultilineParamDescription(self.indentation))

        if self.include_sentence_capitalization:
            _filters.append(SentenceCapitalization(self.prefixes))

        return _filters

    @property
    def verbs(self) -> Tuple[str]:
        """
        Returns the filtered verbs. Ignored verbs are not included.

        :return: Tuple of verbs.
        """

        return tuple([verb for verb in self._verbs if verb not in self.ignored_verbs])

    @classmethod
    def from_json(cls, json_path: Path) -> "DocstringFormatterConfig":
        """
        Creates a new instance from a JSON file.

        :param json_path: Path to the JSON file.
        :return: New instance.
        """

        with open(json_path, "r") as file:
            data = json.load(file)

        new_config = cls(**data)

        # convert all lists to tuples
        for key, value in data.items():
            if isinstance(value, list):
                setattr(new_config, key, tuple(value))

        return new_config

    def to_json(self, json_path: Path) -> None:
        """
        Saves the current instance to a JSON file.

        :param json_path: Path to the JSON file.
        """

        with open(json_path, "w") as file:
            json.dump(self.__dict__, file, indent=4)
