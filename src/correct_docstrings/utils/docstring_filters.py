"""
Collection of filters for a single docstring.
"""
import string
from abc import ABC
from typing import List, Tuple


class DocstringFilterBase(ABC):
    def format(self, content: List[str]) -> List[str]:
        """
        Formats the content.

        :param content: list of lines in the file.
        :return: formatted list of lines in the file.
        """
        pass


class EmptyLineBetweenDescriptionAndParams(DocstringFilterBase):
    """
    make sure empty line between description and list of params
    find first param in docstring and check if there is description above it
    if so, make sure that there is empty line between description and param list

    :return: list of lines in docstring
    """

    def format(self, docstring: List[str]):
        prefixes = [":param", ":return", ":raises"]
        start_of_param_list = -1
        docstring = docstring.copy()

        for i in range(len(docstring)):
            line = docstring[i].strip()
            # check if it starts with prefix
            for prefix in prefixes:
                if line.startswith(prefix) and i > 1:
                    start_of_param_list = i
                    break

            if start_of_param_list != -1:
                break

        if start_of_param_list == -1:
            return docstring

        # remove all empty lines before param list and enter a single empty line
        # before param list
        while docstring[start_of_param_list - 1].strip() == "":
            docstring.pop(start_of_param_list - 1)
            start_of_param_list -= 1

        docstring.insert(start_of_param_list, "")

        return docstring


class RemoveUnwantedPrefixes(DocstringFilterBase):
    """
    Make sure that lines that contain :param or :return or :raises are prefixed with ": "
       and there are no unnecessary prefixes, only whitespace is allowed before the prefix
    """

    def format(self, docstring: List[str]) -> List[str]:
        prefixes = [":param", ":return", ":raises"]

        for i in range(len(docstring)):
            line = docstring[i]
            # check if one prefixes is in line
            for prefix in prefixes:
                index = line.find(prefix)
                if index != -1:
                    # make sure there is only whitespace before prefix
                    # replace all characters before prefix with whitespace
                    docstring[i] = " " * index + line[index:]
                    break

        return docstring


class NoRepeatedWhitespaces(DocstringFilterBase):
    def format(self, docstring: List[str]) -> List[str]:
        prefixes = [":param", ":return", ":raises"]
        for i in range(len(docstring)):
            line = docstring[i]
            for prefix in prefixes:
                index = line.find(prefix)
                if index != -1:
                    index_of_second_semicolon = line.find(":", index + len(prefix))
                    if index_of_second_semicolon != -1:
                        line_after_second_semicolon = line[
                            index_of_second_semicolon + 1 :
                        ]

                        while line_after_second_semicolon.startswith(" "):
                            line_after_second_semicolon = line_after_second_semicolon[
                                1:
                            ]

                        if len(line_after_second_semicolon) > 1:
                            line_after_second_semicolon = (
                                " "
                                + line_after_second_semicolon[0].upper()
                                + line_after_second_semicolon[1:]
                            )

                        docstring[i] = (
                            line[: index_of_second_semicolon + 1]
                            + line_after_second_semicolon
                        )

        return docstring


class EndOfSentencePunctuation(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that each sentence ends
    with a punctuation mark.
    """

    def __init__(self, punctuation: str = "."):
        self.punctuation = punctuation

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that each sentence ends with a punctuation mark. If a sentence
        spans multiple lines, the last line of the sentence is the one that ends
        with a punctuation mark.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for i in range(len(docstring)):
            line = docstring[i].strip()
            if not line:
                continue

            if line.endswith(self.punctuation):
                continue

            if not any(char.isalpha() for char in line):
                continue

            if line[-1] in string.punctuation:
                continue

            if i + 1 >= len(docstring):
                docstring[i] = docstring[i].rstrip() + self.punctuation
                continue

            j = i + 1
            next_line = docstring[j].strip()

            while not next_line and j < len(docstring):
                next_line = docstring[j].strip()
                j += 1

            if next_line.startswith(":") or j + 1 >= len(docstring):
                docstring[i] = docstring[i].rstrip() + self.punctuation

        return docstring


class EnsureColonInParamDescription(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that each parameter description
    starts with ':param <param_name>:'.
    """

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that each parameter description starts with ':param <param_name>:'.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for i, line in enumerate(docstring):
            if not line:
                continue

            if line.strip().startswith(":param") and (
                line.count(":") == 1 or len(line.strip().split(":")[1].split(" ")) != 2
            ):
                j = line.index(":")
                # find the second word in the line after j and add a colon after it
                j += line[j + 1 :].index(" ") + 1
                j += line[j + 1 :].index(" ") + 1
                docstring[i] = line[:j] + line[j:].replace(" ", ": ", 1)

            while "::" in docstring[i]:
                docstring[i] = docstring[i].replace("::", ":")

        return docstring


class IndentMultilineParamDescription(DocstringFilterBase):
    def __init__(self, indentation: str = " " * 2):
        self.indentation = indentation

    def format(self, docstring: List[str]) -> List[str]:

        for i, line in enumerate(docstring):
            if not line:
                continue

            next_line = docstring[i + 1] if i + 1 < len(docstring) else None
            if not next_line:
                continue

            j = 0
            while line.strip().startswith(
                ":param"
            ) and not next_line.strip().startswith(":"):
                j += 1
                next_line = docstring[i + j] if i + j < len(docstring) else None

                if not next_line or next_line.strip().startswith(":"):
                    j -= 1
                    break

            default_indentation = " " * (len(line) - len(line.lstrip()))
            for k in range(j):
                index = i + k + 1
                if index >= len(docstring):
                    break
                docstring[index] = (
                    default_indentation + self.indentation + docstring[index].lstrip()
                )

        return docstring


class ThirdPersonConverter(DocstringFilterBase):
    """ """

    def __init__(self):
        self.blocking_words = "not, to, a, an, the, for, in, of, and, or, as, if, but, nor, so, yet, at, by, from, into, like, over, after, before, between, into, through, with, without, during, without, until, up, upon, about, above, across, after, against, along, amid, among, anti, around, as, at, before, behind, below, beneath, beside, besides, between, beyond, concerning, considering, despite, down, during, except, excepting, excluding, following, for, from, in, inside, into, like, minus, near, of, off, on, onto, opposite, outside, over, past, per, plus, regarding, round, save, since, than, through, to, toward, towards, under, underneath, unlike, until, up, upon, versus, via, with, within, without".split(
            ", "
        )
        self.modals = ["can", "must", "should", "may", "might"]
        self.verbs = "abide, accelerate, accept, accomplish, achieve, acquire, acted, activate, adapt, add, address, administer, admire, admit, adopt, advise, afford, agree, alert, alight, allow, altered, amuse, analyze, announce, annoy, answer, anticipate, apologize, appear, applaud, applied, appoint, appraise, appreciate, approve, arbitrate, argue, arise, arrange, arrest, arrive, ascertain, ask, assemble, assess, assist, assure, attach, attack, attain, attempt, attend, attract, audited, avoid, awake, back, bake, balance, ban, bang, bare, bat, bathe, battle, be, beam, bear, beat, become, beg, begin, behave, behold, belong, bend, beset, bet, bid, bind, bite, bleach, bleed, bless, blind, blink, blot, blow, blush, boast, boil, bolt, bomb, book, bore, borrow, bounce, bow, box, brake, branch, break, breathe, breed, brief, bring, broadcast, bruise, brush, bubble, budget, build, bump, burn, burst, bury, bust, buy, buze, calculate, call, can, camp, care, carry, carve, cast, catalog, catch, cause, challenge, change, charge, chart, chase, cheat, check, cheer, chew, choke, choose, chop, claim, clap, clarify, classify, clean, clear, cling, clip, close, clothe, coach, coil, collect, color, comb, come, command, communicate, compare, compete, compile, complain, complete, compose, compute, conceive, concentrate, conceptualize, concern, conclude, conduct, confess, confront, confuse, connect, conserve, consider, consist, consolidate, construct, consult, contain, continue, contract, control, convert, coordinate, copy, correct, correlate, cost, cough, counsel, count, cover, crack, crash, crawl, create, creep, critique, cross, crush, cry, cure, curl, curve, cut, cycle, dam, damage, dance, dare, deal, decay, deceive, decide, decorate, define, delay, delegate, delight, deliver, demonstrate, depend, describe, desert, deserve, design, destroy, detail, detect, determine, develop, devise, diagnose, dig, direct, disagree, disappear, disapprove, disarm, discover, dislike, dispense, display, disprove, dissect, distribute, dive, divert, divide, do, double, doubt, draft, drag, drain, dramatize, draw, dream, dress, drink, drip, drive, drop, drown, drum, dry, dust, dwell, earn, eat, edited, educate, eliminate, embarrass, employ, empty, enacted, encourage, end, endure, enforce, engineer, enhance, enjoy, enlist, ensure, enter, entertain, escape, establish, estimate, evaluate, examine, exceed, excite, excuse, execute, exercise, exhibit, exist, expand, expect, expedite, experiment, explain, explode, express, extend, extract, face, facilitate, fade, fail, fancy, fasten, fax, fear, feed, feel, fence, fetch, fight, file, fill, film, finalize, finance, find, fire, fit, fix, flap, flash, flee, fling, float, flood, flow, flower, fly, fold, follow, fool, forbid, force, forecast, forego, foresee, foretell, forget, forgive, form, formulate, forsake, frame, freeze, frighten, fry, gather, gaze, generate, get, give, glow, glue, go, govern, grab, graduate, grate, grease, greet, grin, grind, grip, groan, grow, guarantee, guard, guess, guide, hammer, hand, handle, handwrite, hang, happen, harass, harm, hate, haunt, head, heal, heap, hear, heat, help, hide, hit, hold, hook, hop, hope, hover, hug, hum, hunt, hurry, hurt, hypothesize, identify, ignore, illustrate, imagine, implement, impress, improve, improvise, include, increase, induce, influence, inform, initiate, inject, injure, inlay, innovate, input, inspect, inspire, install, institute, instruct, insure, integrate, intend, intensify, interest, interfere, interlay, interpret, interrupt, interview, introduce, invent, inventory, investigate, invite, irritate, itch, jail, jam, jog, join, joke, judge, juggle, jump, justify, keep, kept, kick, kill, kiss, kneel, knit, knock, knot, know, label, land, last, laugh, launch, lay, lead, lean, leap, learn, leave, lecture, led, lend, let, level, license, lick, lie, lifted, light, lighten, like, list, listen, live, load, locate, lock, log, long, look, lose, love, maintain, make, man, manage, manipulate, manufacture, map, march, mark, market, marry, match, mate, matter, mean, measure, meddle, mediate, meet, melt, melt, memorize, mend, mentor, milk, mine, mislead, miss, misspell, mistake, misunderstand, mix, moan, model, modify, monitor, moor, motivate, mourn, move, mow, muddle, mug, multiply, murder, nail, name, navigate, need, negotiate, nest, nod, nominate, normalize, note, notice, number, obey, object, observe, obtain, occur, offend, offer, officiate, open, operate, order, organize, oriented, originate, overcome, overdo, overdraw, overflow, overhear, overtake, overthrow, overwrite, owe, own, pack, paddle, paint, park, part, participate, pass, paste, pat, pause, pay, peck, pedal, peel, peep, perceive, perfect, perform, permit, persuade, phone, photograph, pick, pilot, pinch, pine, pinpoint, pioneer, place, plan, plant, play, plead, please, plug, point, poke, polish, pop, possess, post, pour, practice, praised, pray, preach, precede, predict, prefer, prepare, prescribe, present, preserve, preset, preside, press, pretend, prevent, prick, print, process, procure, produce, profess, program, progress, project, promise, promote, proofread, propose, protect, prove, provide, publicize, pull, pump, punch, puncture, punish, purchase, push, put, qualify, question, queue, quit, race, radiate, rain, raise, rank, rate, reach, read, realign, realize, reason, receive, recognize, recommend, reconcile, record, recruit, reduce, refer, reflect, refuse, regret, regulate, rehabilitate, reign, reinforce, reject, rejoice, relate, relax, release, rely, remain, remember, remind, remove, render, reorganize, repair, repeat, replace, reply, report, represent, reproduce, request, rescue, research, resolve, respond, restored, restructure, retire, retrieve, return, review, revise, rhyme, rid, ride, ring, rinse, rise, risk, rob, rock, roll, rot, rub, ruin, rule, run, rush, sack, sail, satisfy, save, saw, say, scare, scatter, schedule, scold, scorch, scrape, scratch, scream, screw, scribble, scrub, seal, search, secure, see, seek, select, sell, send, sense, separate, serve, service, set, settle, sew, shade, shake, shape, share, shave, shear, shed, shelter, shine, shiver, shock, shoe, shoot, shop, show, shrink, shrug, shut, sigh, sign, signal, simplify, sin, sing, sink, sip, sit, sketch, ski, skip, slap, slay, sleep, slide, sling, slink, slip, slit, slow, smash, smell, smile, smite, smoke, snatch, sneak, sneeze, sniff, snore, snow, soak, solve, soothe, soothsay, sort, sound, sow, spare, spark, sparkle, speak, specify, speed, spell, spend, spill, spin, spit, split, spoil, spot, spray, spread, spring, sprout, squash, squeak, squeal, squeeze, stain, stamp, stand, stare, start, stay, steal, steer, step, stick, stimulate, sting, stink, stir, stitch, stop, store, strap, streamline, strengthen, stretch, stride, strike, string, strip, strive, stroke, structure, study, stuff, sublet, subtract, succeed, suck, suffer, suggest, suit, summarize, supervise, supply, support, suppose, surprise, surround, suspect, suspend, swear, sweat, sweep, swell, swim, swing, switch, symbolize, synthesize, systemize, tabulate, take, talk, tame, tap, target, taste, teach, tear, tease, telephone, tell, tempt, terrify, test, thank, thaw, think, thrive, throw, thrust, tick, tickle, tie, time, tip, tire, touch, tour, tow, trace, trade, train, transcribe, transfer, transform, translate, transport, trap, travel, tread, treat, tremble, trick, trip, trot, trouble, troubleshoot, trust, try, tug, tumble, turn, tutor, twist, type, undergo, understand, undertake, undress, unfasten, unify, unite, unlock, unpack, untidy, update, upgrade, uphold, upset, use, utilize, vanish, verbalize, verify, vex, visit, wail, wait, wake, walk, wander, want, warm, warn, wash, waste, watch, water, wave, wear, weave, wed, weep, weigh, welcome, wend, wet, whine, whip, whirl, whisper, whistle, win, wind, wink, wipe, wish, withdraw, withhold, withstand, wobble, wonder, work, worry, wrap, wreck, wrestle, wriggle, wring, write, x-ray, yawn, yell, zip, zoom, validate".split(
            ", "
        )

    def format(self, docstring):
        """ """
        # check which line starts with ":"
        end_index = -1
        for i in range(len(docstring)):
            line = docstring[i].strip()
            if line.startswith(":"):
                end_index = i
                break

        if end_index == -1:
            return docstring

        for i in range(1, end_index):
            line = docstring[i]
            leading_whitespaces = len(line) - len(line.lstrip())
            new_line = " " * leading_whitespaces
            previous_word = ""
            for word in line.split():
                word, punctuation = ThirdPersonConverter.split_punctuation(word)
                if (
                    previous_word.lower() not in self.blocking_words
                    and previous_word.lower() not in self.verbs
                    and not previous_word.lower().endswith("n't")
                ):
                    word = self.convert_to_third_person_singular(word)
                new_line += word + punctuation + " "
                previous_word = word

            docstring[i] = new_line.rstrip()

        return docstring

    def convert_to_third_person_singular(self, word: str) -> str:
        """
        Convert word to third-person singular form.

        :param word: word to convert.
        :return: third-person singular form of word.
        """
        if not self.is_verb(word):
            return word
        if word.lower() in self.modals:
            return word

        # Add –es instead of –s if the base form ends in -s, -z, -x, -sh, -ch, or the vowel o (but not -oo).

        if (
            word.lower()[-1]
            in [
                "s",
                "z",
                "x",
                "sh",
                "ch",
                "o",
            ]
            and not word.lower().endswith("oo")
        ):
            return word + "es"

        # If the base form ends in consonant + y, remove the -y and add –ies.
        if word.lower()[-1] == "y":
            return word[:-1] + "ies"

        return word + "s"

    def is_verb(self, word: str) -> bool:
        """
        Check if word is a verb

        :param word: word to check
        :return: True if word is a verb, False otherwise
        """
        return word.lower().strip() in self.verbs

    @staticmethod
    def split_punctuation(word: str) -> Tuple[str, str]:
        """
        Split word into two parts: word and punctuation

        :param word: word to split
        :return: word and punctuation
        """
        letters = ""

        end_index = -1
        for i, letter in enumerate(word):
            if not letter.isalpha():
                end_index = i
                break
            letters += letter

        punctuation = word[end_index:] if end_index != -1 else ""

        return letters, punctuation


class DocstringFormatter:
    def __init__(self):
        self.filters = [
            EmptyLineBetweenDescriptionAndParams(),
            NoRepeatedWhitespaces(),
            RemoveUnwantedPrefixes(),
            ThirdPersonConverter(),
            EndOfSentencePunctuation(),
            EnsureColonInParamDescription(),
            IndentMultilineParamDescription(),
        ]

    def format(self, docstring) -> str:

        for docstring_filter in self.filters:
            docstring = docstring_filter.format(docstring)

        return docstring
