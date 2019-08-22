# -*- coding: utf-8 -*-

import xterm_keys

from tui_task import TaskState

from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.formatted_text import to_formatted_text, HTML
from prompt_toolkit.formatted_text.utils import fragment_list_to_text
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings, ConditionalKeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame, RadioList, VerticalLine, HorizontalLine, TextArea
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.document import Document

import itertools
from ast import literal_eval

import app_loggers
logger = app_loggers.tui_logger


class FormatTextHTML(Processor):
    """Here: https://github.com/prompt-toolkit/python-prompt-toolkit/issues/711
       and also in SRU_com
    """
    def apply_transformation(self, ti):
        try:
            fragments = to_formatted_text(HTML(fragment_list_to_text(ti.fragments)))
        except Exception as ex:
            # xml.parsers.expat.ExpatError
            # not well-formed (invalid token): line 1, column 138
            logger.error('FormatText: {} {}'.format(type(ex), str(ex)))
            #return Transformation([('', ' ')])
            return Transformation([])
        return Transformation(fragments)


class TuiApp:
    def __init__(self, config, out_queue, state=TaskState()):
        self.config = config
        tui_config = config['tui']
        self.tui_config = tui_config
        self.out_queue = out_queue


        def commandHandler(buffer):
            #check incoming command
            cmdString = buffer.text
            #executeCommand(cmdString)
            pass


        def commandPrompt(line_number, wrap_count):
            return "command> "

        ########################################################################

        kb = KeyBindings()

        @kb.add('c-d')
        def exit_(event):
            """
            Pressing Esc will exit the user interface.

            Setting a return value means: quit the event loop that drives the user
            interface and return this value from the `CommandLineInterface.run()` call.
            """
            event.app.exit()

        @kb.add('tab')
        def tab_(event):
            focus_next(event)

        @kb.add('s-tab')
        def stab_(event):
            focus_previous(event)

        @kb.add('s-right')
        def next_tab(event):
            state.next_tab()
            event.app.invalidate()

        @kb.add('s-left')
        def next_tab(event):
            state.prev_tab()
            event.app.invalidate()


        orders_kb = KeyBindings()
        @orders_kb.add('f5')
        def _(event):
            #command = ('refresh', something...)
            #self.out_queue.put_nowait(command)
            pass

        ########################################################################

        outputArea = TextArea(text="", 
                    multiline=True,
                    wrap_lines=False,
                    #lexer=lexer.OutputAreaLexer(),
                    #scrollbar=enableScrollbar,
                    style='class:output-field',
                    read_only=True)

        content_container = Frame(outputArea, title="Output")

        log_container = Frame(
            Window(
                BufferControl(
                    buffer=Buffer(name='logger_buffer', read_only=True),
                    input_processors=[FormatTextHTML()],
                ),
                right_margins=[ScrollbarMargin(display_arrows=True)], # low-level scrollbar
            ),
            title='Log',
            height=8,
        )

        command_container = TextArea(
            text="",
            multiline=False,
            accept_handler=commandHandler,
            get_line_prefix=commandPrompt
        )

        commandWindowFrame= Frame(
            command_container,
            title="TuiTerminal (Ctrl-D to exit, Tab to switch focus and refresh UI, 'help' for help)",
            height=4
        )

        root_container = HSplit([content_container, log_container, commandWindowFrame])

        layout = Layout(root_container, focused_element=command_container)

        style = Style.from_dict(
            {
                'output-field': 'bg:#101010',
                'frame.border': 'SteelBlue',
                'frame.label': 'PowderBlue',
            }
        )

        application = Application(
            layout=layout,
            key_bindings=kb,
            style=style,
            full_screen=tui_config.getboolean('full_screen'),
            mouse_support=tui_config.getboolean('mouse_support'),
            #after_render=after_render,
        )

        self.application = application



def make_tui_app(config, out_queue, state=TaskState()):
    application = TuiApp(config, out_queue, state)
    return application
