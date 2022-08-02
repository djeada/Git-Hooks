from dataclasses import dataclass
import sys
from pathlib import Path
from typing import List, Tuple


@dataclass
class DocstringFormatterConfig:
    """
    Configuration for the docstring formatter.
    """
    docstring: Tuple[str] = tuple()


@dataclass
class TypeHintFormatterConfig:
    """
    Configuration for the type hint formatter.
    """
    content: str = ""


@dataclass
class ScriptFormatterConfig:
    """
    Configuration for the script formatter.
    """
    path: Path
    print_diff: bool = False
    in_place: bool = False
    docstring_formatter_config: DocstringFormatterConfig = DocstringFormatterConfig()


class ScriptFormatterConfigFactory:

    @staticmethod
    def from_json(json_str: str) -> ScriptFormatterConfig:
        """
        Create a ScriptFormatterConfig from a JSON string.
        """
        pass

    @staticmethod
    def from_args(args: List[str]) -> ScriptFormatterConfig:
        """
        Create a ScriptFormatterConfig from command line arguments.
        """
        pass


class ScriptFormatter:
    def __init__(self, config: ScriptFormatterConfig):
        if not config.path.is_file():
            return

        self.content = config.path.read_text()

        content_as_list = self.add_missing_docstrings()
        # content_as_list = assert_optional_type_hints(content_as_list.copy())
        content = "\n".join(content_as_list)

        next_docstring_pos = self.find_next_docstring(0)
        while next_docstring_pos != (-1, -1):
            start_pos, end_pos = next_docstring_pos
            docstring = content.split("\n")[start_pos: end_pos + 1]
            docstring = DocstringFormatter(DocstringFormatterConfig(docstring)).format()
            content_list_of_lines = content.split("\n")
            content_list_of_lines = (
                    content_list_of_lines[:start_pos]
                    + docstring
                    + content_list_of_lines[end_pos + 1:]
            )
            content = "\n".join(content_list_of_lines)

            next_docstring_pos = self.find_next_docstring(start_pos + len(docstring) + 1
                                                          )

        config.path.write_text(content)

    def add_missing_docstrings(self) -> List[str]:
        """
        Add docstring to file.
        :return: list of lines in file
        """

        possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]

        i = 0
        content = self.content.split("\n").copy()
        while i < len(content) - 1:
            line = content[i].strip()
            indentation = len(content[i]) - len(content[i].lstrip()) + 4
            if line.startswith("def"):
                end_index = i
                while not line.endswith(":"):
                    end_index += 1
                    line = content[end_index].strip()

                if content[end_index + 1].strip() not in possible_docstring_start:
                    # find the parameters of the function between ()

                    parameters = Utils.extract_parameters(content, i, end_index)

                    # add docstring
                    content.insert(end_index + 1, f'{" " * indentation}"""')
                    content.insert(
                        end_index + 2, f'{" " * indentation}Description of function \n'
                    )
                    # add parameters
                    end_index += 3
                    for parameter in parameters:
                        parameter = parameter.split(":")[0]
                        content.insert(
                            end_index, f'{" " * indentation}:param {parameter.strip()}:'
                        )
                        end_index += 1
                    # add return
                    content.insert(end_index, f'{" " * indentation}:return:')
                    content.insert(end_index + 1, f'{" " * indentation}"""')
            i += 1

        return content

    def find_next_docstring(self, index: int) -> Tuple[int, int]:
        """
        Finds next docstring in content starting from index. Returns (-1, -1) if no docstring found.

        :param index: index to start looking for docstring
        :return: start and end position of docstring
        """
        possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]
        corresponding_docstring_end = {
            '"""': '"""',
            "'''": "'''",
            'r"""': '"""',
            "r'''": "'''",
        }

        content = self.content.split("\n")
        for i in range(index, len(content)):
            line = content[i].strip()
            if line in possible_docstring_start:
                for j in range(i + 1, len(content)):
                    next_line = content[j].strip()
                    if next_line == corresponding_docstring_end[line]:
                        return i, j

        return -1, -1

    def preserve_parameter_order(self) -> List[str]:
        """
        """
        content = self.content.split("\n").copy()
        start_index, end_index = self.find_next_docstring(0)

        if start_index == -1:
            return content

        # find the index of first 'def' above start_index
        i = start_index - 1
        while i >= 0:
            line = content[i].strip()
            if line.startswith("def"):
                break
            i -= 1

        if i == -1:
            return content

        parameters_from_function = Utils.extract_parameters(content, i, start_index)

        docstring = content[start_index: end_index + 1]
        parameters_from_docstring = []

        for line in docstring:
            if line.strip().startswith(":param"):
                parameters_from_docstring.append(line)

        # order of parameters in docstring must match the order of parameters in parameters
        for i, parameter in enumerate(parameters_from_function):
            parameter_name = parameter.split(":")[0].strip()
            # find in which line the parameter in parameters_from_docstring is
            flag = False
            for j, line in enumerate(parameters_from_docstring):
                if f":param {parameter_name}" in line:
                    if i != j:
                        # swap j and i if i < len(parameters_from_docstring)
                        if i < len(parameters_from_docstring):
                            parameters_from_docstring[j], parameters_from_docstring[i] = parameters_from_docstring[i], \
                                                                                         parameters_from_docstring[j]
                        else:
                            flag = True
                    break
            if flag:
                # add parameter to docstring if it is not in docstring
                parameters_from_docstring.insert(i, f":param {parameter_name}:")

        # remove all lines starting with :param from docstring
        for i, line in reversed(list(enumerate(docstring.copy()))):
            if line.strip().startswith(":param"):
                docstring.pop(i)

        # remove the last line of docstring if it starts with :return:
        n = len(docstring) - 1
        if n > 0 and docstring[n - 1].strip().startswith(":return"):
            n -= 1
        if n < 0:
            n = 0

        # append parameters from parameters_from_docstring to docstring
        for parameter in parameters_from_docstring:
            docstring.insert(n, parameter)
            n += 1

        content[start_index: end_index + 1] = docstring
        return content


class TypeHintsFormatter:
    def __init__(self, config: TypeHintFormatterConfig):
        self.content = config.content

    def optional_type_hints(self) -> List[str]:
        """
        Find parameters with default value None and add Optional[type] to them.

        :return: list of lines in file
        """

        i = 0
        content = self.content.split("\n").copy()
        while i < len(content) - 1:
            line = content[i].strip()

            if line.startswith("def"):
                end_index = i
                while not line.endswith(":"):
                    end_index += 1
                    line = content[end_index].strip()

                parameters = Utils.extract_parameters(content, i, end_index)

                # find the parameters with default value None
                parameters_with_default_value_none = [
                    parameter for parameter in parameters if "= None" in parameter
                ]
                # add Optional[type] to parameters with default value None
                for parameter in parameters_with_default_value_none:
                    parameter_name = parameter.split(":")[0].strip()
                    parameter_type = parameter.split(":")[1].strip()
                    parameter_type = parameter_type.replace("= None", "").rstrip()
                    for j in range(i, end_index + 1):
                        content[j] = content[j].replace(
                            parameter,
                            f"{parameter_name}: Optional[{parameter_type}] = None",
                        )

            i += 1

        return content


class DocstringFormatter:
    def __init__(self, config: DocstringFormatterConfig):
        self.docstring = config.docstring

    def format(self) -> str:
        self.docstring = self.empty_line_between_description_and_param_list()
        self.docstring = self.no_unnecessary_prefixes()
        self.docstring = self.single_whitespace_after_second_semicolon()
        # docstring = convert_to_third_person(docstring.copy())
        return self.docstring

    def single_whitespace_after_second_semicolon(self) -> List[str]:
        """
        Find the lines containing prefixes = [":param", ":return", ":raises"].
        For those lines make sure that there is only one whitespace after the second semicolon.

        :return: list of lines in docstring
        """
        prefixes = [":param", ":return", ":raises"]
        docstring = self.docstring.copy()
        for i in range(len(docstring)):
            line = docstring[i]
            for prefix in prefixes:
                index = line.find(prefix)
                if index != -1:
                    index_of_second_semicolon = line.find(":", index + len(prefix))
                    if index_of_second_semicolon != -1:
                        line_after_second_semicolon = line[index_of_second_semicolon + 1:]

                        while line_after_second_semicolon.startswith(" "):
                            line_after_second_semicolon = line_after_second_semicolon[1:]

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

    def empty_line_between_description_and_param_list(self,

                                                      ) -> List[str]:
        """
        make sure empty line between description and list of params
        find first param in docstring and check if there is description above it
        if so, make sure that there is empty line between description and param list

        :return: list of lines in docstring
        """
        prefixes = [":param", ":return", ":raises"]
        start_of_param_list = -1
        docstring = self.docstring.copy()

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

    def no_unnecessary_prefixes(self) -> List[str]:
        """
        Make sure that lines that contain :param or :return or :raises are prefixed with ": "
        and there are no unnecessary prefixes, only whitespace is allowed before the prefix

        :return: list of lines in docstring
        """
        prefixes = [":param", ":return", ":raises"]
        docstring = self.docstring.copy()

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


class ThirdPersonConverter:
    """
    """

    def __init__(self, content: str):
        self.content = content
        self.blocking_words = "not, to, a, an, the, for, in, of, and, or, as, if, but, nor, so, yet, at, by, from, into, like, over, after, before, between, into, through, with, without, during, without, until, up, upon, about, above, across, after, against, along, amid, among, anti, around, as, at, before, behind, below, beneath, beside, besides, between, beyond, concerning, considering, despite, down, during, except, excepting, excluding, following, for, from, in, inside, into, like, minus, near, of, off, on, onto, opposite, outside, over, past, per, plus, regarding, round, save, since, than, through, to, toward, towards, under, underneath, unlike, until, up, upon, versus, via, with, within, without".split(
            ", ")
        self.modals = ['can', 'must', 'should', 'may', 'might']
        self.verbs = "abide, accelerate, accept, accomplish, achieve, acquire, acted, activate, adapt, add, address, administer, admire, admit, adopt, advise, afford, agree, alert, alight, allow, altered, amuse, analyze, announce, annoy, answer, anticipate, apologize, appear, applaud, applied, appoint, appraise, appreciate, approve, arbitrate, argue, arise, arrange, arrest, arrive, ascertain, ask, assemble, assess, assist, assure, attach, attack, attain, attempt, attend, attract, audited, avoid, awake, back, bake, balance, ban, bang, bare, bat, bathe, battle, be, beam, bear, beat, become, beg, begin, behave, behold, belong, bend, beset, bet, bid, bind, bite, bleach, bleed, bless, blind, blink, blot, blow, blush, boast, boil, bolt, bomb, book, bore, borrow, bounce, bow, box, brake, branch, break, breathe, breed, brief, bring, broadcast, bruise, brush, bubble, budget, build, bump, burn, burst, bury, bust, buy, buze, calculate, call, can, camp, care, carry, carve, cast, catalog, catch, cause, challenge, change, charge, chart, chase, cheat, check, cheer, chew, choke, choose, chop, claim, clap, clarify, classify, clean, clear, cling, clip, close, clothe, coach, coil, collect, color, comb, come, command, communicate, compare, compete, compile, complain, complete, compose, compute, conceive, concentrate, conceptualize, concern, conclude, conduct, confess, confront, confuse, connect, conserve, consider, consist, consolidate, construct, consult, contain, continue, contract, control, convert, coordinate, copy, correct, correlate, cost, cough, counsel, count, cover, crack, crash, crawl, create, creep, critique, cross, crush, cry, cure, curl, curve, cut, cycle, dam, damage, dance, dare, deal, decay, deceive, decide, decorate, define, delay, delegate, delight, deliver, demonstrate, depend, describe, desert, deserve, design, destroy, detail, detect, determine, develop, devise, diagnose, dig, direct, disagree, disappear, disapprove, disarm, discover, dislike, dispense, display, disprove, dissect, distribute, dive, divert, divide, do, double, doubt, draft, drag, drain, dramatize, draw, dream, dress, drink, drip, drive, drop, drown, drum, dry, dust, dwell, earn, eat, edited, educate, eliminate, embarrass, employ, empty, enacted, encourage, end, endure, enforce, engineer, enhance, enjoy, enlist, ensure, enter, entertain, escape, establish, estimate, evaluate, examine, exceed, excite, excuse, execute, exercise, exhibit, exist, expand, expect, expedite, experiment, explain, explode, express, extend, extract, face, facilitate, fade, fail, fancy, fasten, fax, fear, feed, feel, fence, fetch, fight, file, fill, film, finalize, finance, find, fire, fit, fix, flap, flash, flee, fling, float, flood, flow, flower, fly, fold, follow, fool, forbid, force, forecast, forego, foresee, foretell, forget, forgive, form, formulate, forsake, frame, freeze, frighten, fry, gather, gaze, generate, get, give, glow, glue, go, govern, grab, graduate, grate, grease, greet, grin, grind, grip, groan, grow, guarantee, guard, guess, guide, hammer, hand, handle, handwrite, hang, happen, harass, harm, hate, haunt, head, heal, heap, hear, heat, help, hide, hit, hold, hook, hop, hope, hover, hug, hum, hunt, hurry, hurt, hypothesize, identify, ignore, illustrate, imagine, implement, impress, improve, improvise, include, increase, induce, influence, inform, initiate, inject, injure, inlay, innovate, input, inspect, inspire, install, institute, instruct, insure, integrate, intend, intensify, interest, interfere, interlay, interpret, interrupt, interview, introduce, invent, inventory, investigate, invite, irritate, itch, jail, jam, jog, join, joke, judge, juggle, jump, justify, keep, kept, kick, kill, kiss, kneel, knit, knock, knot, know, label, land, last, laugh, launch, lay, lead, lean, leap, learn, leave, lecture, led, lend, let, level, license, lick, lie, lifted, light, lighten, like, list, listen, live, load, locate, lock, log, long, look, lose, love, maintain, make, man, manage, manipulate, manufacture, map, march, mark, market, marry, match, mate, matter, mean, measure, meddle, mediate, meet, melt, melt, memorize, mend, mentor, milk, mine, mislead, miss, misspell, mistake, misunderstand, mix, moan, model, modify, monitor, moor, motivate, mourn, move, mow, muddle, mug, multiply, murder, nail, name, navigate, need, negotiate, nest, nod, nominate, normalize, note, notice, number, obey, object, observe, obtain, occur, offend, offer, officiate, open, operate, order, organize, oriented, originate, overcome, overdo, overdraw, overflow, overhear, overtake, overthrow, overwrite, owe, own, pack, paddle, paint, park, part, participate, pass, paste, pat, pause, pay, peck, pedal, peel, peep, perceive, perfect, perform, permit, persuade, phone, photograph, pick, pilot, pinch, pine, pinpoint, pioneer, place, plan, plant, play, plead, please, plug, point, poke, polish, pop, possess, post, pour, practice, praised, pray, preach, precede, predict, prefer, prepare, prescribe, present, preserve, preset, preside, press, pretend, prevent, prick, print, process, procure, produce, profess, program, progress, project, promise, promote, proofread, propose, protect, prove, provide, publicize, pull, pump, punch, puncture, punish, purchase, push, put, qualify, question, queue, quit, race, radiate, rain, raise, rank, rate, reach, read, realign, realize, reason, receive, recognize, recommend, reconcile, record, recruit, reduce, refer, reflect, refuse, regret, regulate, rehabilitate, reign, reinforce, reject, rejoice, relate, relax, release, rely, remain, remember, remind, remove, render, reorganize, repair, repeat, replace, reply, report, represent, reproduce, request, rescue, research, resolve, respond, restored, restructure, retire, retrieve, return, review, revise, rhyme, rid, ride, ring, rinse, rise, risk, rob, rock, roll, rot, rub, ruin, rule, run, rush, sack, sail, satisfy, save, saw, say, scare, scatter, schedule, scold, scorch, scrape, scratch, scream, screw, scribble, scrub, seal, search, secure, see, seek, select, sell, send, sense, separate, serve, service, set, settle, sew, shade, shake, shape, share, shave, shear, shed, shelter, shine, shiver, shock, shoe, shoot, shop, show, shrink, shrug, shut, sigh, sign, signal, simplify, sin, sing, sink, sip, sit, sketch, ski, skip, slap, slay, sleep, slide, sling, slink, slip, slit, slow, smash, smell, smile, smite, smoke, snatch, sneak, sneeze, sniff, snore, snow, soak, solve, soothe, soothsay, sort, sound, sow, spare, spark, sparkle, speak, specify, speed, spell, spend, spill, spin, spit, split, spoil, spot, spray, spread, spring, sprout, squash, squeak, squeal, squeeze, stain, stamp, stand, stare, start, stay, steal, steer, step, stick, stimulate, sting, stink, stir, stitch, stop, store, strap, streamline, strengthen, stretch, stride, strike, string, strip, strive, stroke, structure, study, stuff, sublet, subtract, succeed, suck, suffer, suggest, suit, summarize, supervise, supply, support, suppose, surprise, surround, suspect, suspend, swear, sweat, sweep, swell, swim, swing, switch, symbolize, synthesize, systemize, tabulate, take, talk, tame, tap, target, taste, teach, tear, tease, telephone, tell, tempt, terrify, test, thank, thaw, think, thrive, throw, thrust, tick, tickle, tie, time, tip, tire, touch, tour, tow, trace, trade, train, transcribe, transfer, transform, translate, transport, trap, travel, tread, treat, tremble, trick, trip, trot, trouble, troubleshoot, trust, try, tug, tumble, turn, tutor, twist, type, undergo, understand, undertake, undress, unfasten, unify, unite, unlock, unpack, untidy, update, upgrade, uphold, upset, use, utilize, vanish, verbalize, verify, vex, visit, wail, wait, wake, walk, wander, want, warm, warn, wash, waste, watch, water, wave, wear, weave, wed, weep, weigh, welcome, wend, wet, whine, whip, whirl, whisper, whistle, win, wind, wink, wipe, wish, withdraw, withhold, withstand, wobble, wonder, work, worry, wrap, wreck, wrestle, wriggle, wring, write, x-ray, yawn, yell, zip, zoom, validate".split(
            ", ")

    def convert(self):
        """
        """
        # check which line starts with ":"
        end_index = -1
        for i in range(len(self.content)):
            line = self.content[i].strip()
            if line.startswith(":"):
                end_index = i
                break

        if end_index == -1:
            return self.content

        for i in range(1, end_index):
            line = self.content[i]
            leading_whitespaces = len(line) - len(line.lstrip())
            new_line = " " * leading_whitespaces
            previous_word = ""
            for word in line.split():
                word, punctuation = ThirdPersonConverter.split_punctuation(word)
                if previous_word.lower() not in self.blocking_words and previous_word.lower() not in self.verbs and not previous_word.lower().endswith("n't"):
                    word = self.convert_to_third_person_singular(word)
                new_line += word + punctuation + " "
                previous_word = word

            self.content[i] = new_line.rstrip()

        return self.content

    def convert_to_third_person_singular(self, word: str) -> str:
        """
        Convert word to third person singular form.

        :param word: word to convert
        :return: third person singular form of word
        """
        if not self.is_verb(word):
            return word
        if word.lower() in self.modals:
            return word
        """
        Add –es instead of –s if the base form ends in -s, -z, -x, -sh, -ch, or the vowel o (but not -oo).
        """
        if word.lower()[-1] in ["s", "z", "x", "sh", "ch", "o"] and not word.lower().endswith("oo"):
            return word + "es"

        """
        If the base form ends in consonant + y, remove the -y and add –ies.
        """
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

class Utils:

    @staticmethod
    def extract_parameters(content: List[str], start_index: int, end_index: int) -> List[str]:
        """
        """
        parameters_text = "".join(content[start_index: end_index + 1]).replace(
            "\n", " "
        )
        parameters_text = parameters_text[
                          parameters_text.find("(") + 1: parameters_text.rfind(")")
                          ]
        parameters = [
            param.strip()
            for param in parameters_text.split(",")
            if param.strip() and not param.strip().endswith("]")
        ]
        return parameters


def main():
    # check if user provided file name
    if len(sys.argv) != 2:
        print("Usage: python correct_sphinx_docstring.py <dir_name>")
        exit()

    # check if file exists
    file_name = sys.argv[1]

    if not Path(file_name).is_dir():
        print("Dir does not exist")
        exit()

    # find all files in directory and make sure last line is empty
    for file in Path(file_name).glob("**/*"):
        if not file.is_file():
            continue
        config = ScriptFormatterConfig(file)
        ScriptFormatter(config)


if __name__ == "__main__":
    main()
