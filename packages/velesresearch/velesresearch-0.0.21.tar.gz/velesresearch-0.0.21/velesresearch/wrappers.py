"""Functions creating objects for survey structure classes"""

from .models import *
from .utils import flatten


def survey(
    *pages: PageModel | list[PageModel],
    createStructure: bool = True,
    buildForPublication: bool = False,
    folderName: str = "survey",
    path: str | Path = os.getcwd(),
    **kwargs,
) -> SurveyModel:
    """Create a survey object

    Args:
        pages (PageModel | list[PageModel]): The pages of the survey.
        createStructure (bool): Whether to create the survey structure. Default is True. Alternatively use `createStructure()` method on the created object.
        buildForPublication (bool): Whether to build the survey for publication. Default is False. Alternatively use `buildForPublication()` method on the created object.
        folderName (str): The name of the folder to create the survey in. Default is 'survey'.
        path (str | Path): The path to create the survey in. Default is the current working directory.
        title (str | None): The title of the survey.
        html (str | None): The HTML content to show after the survey is completed.
        locale (str): The locale of the survey. Default is 'en'.
        firstPageIsStarted (bool): Whether the first page is a start page.
        addCode (dict | None): Additional code for the survey. Usually not necessary.
    """
    pages = flatten(pages)
    survey = SurveyModel(pages=pages, **kwargs)
    if buildForPublication:
        survey.buildForProduction(path=path, folderName=folderName)
    elif createStructure:
        survey.createStructure(path=path, folderName=folderName)
    return survey


def page(
    name: str, *questions: QuestionModel | list[QuestionModel], **kwargs
) -> PageModel:
    """Create a page object

    Args:
        name (str): The label of the page.
        questions (QuestionModel | list[QuestionModel]): The questions on the page.
        description (str | None): Optional subtitle or description of the page.
        enableIf (str | None): Expression to enable the page.
        id (str | None): HTML id attribute for the page. Usually not necessary.
        isRequired (bool): Whether the page is required (at least one question must be answered).
        maxTimeToFinish (int | None): Maximum time in seconds to finish the page.
        maxWidth (str): Maximum width of the page in CSS units.
        minWidth (str): Minimum width of the page in CSS units.
        navigationButtonsVisibility (str): The visibility of the navigation buttons. Can be 'inherit', 'show', 'hide'.
        navigationDescription (str | None): Description for the page navigation.
        navigationTitle (str | None): Title for the page navigation.
        questionErrorLocation (str): The location of the error text for the questions. Can be 'default', 'top', 'bottom'.
        questionTitleLocation (str): The location of the title for the questions. Can be 'default', 'top', 'bottom'.
        questionsOrder (str): The order of the questions. Can be 'default', 'random'.
        readOnly (bool): Whether the page is read-only.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the page required (at least one question must be answered).
        state (str): If the page should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        title (str): The visible title of the page.
        visible (bool): Whether the page is visible.
        visibleIf (str | None): Expression to make the page visible.
        visibleIndex (int | None): The index at which the page should be visible.
        width (str): Width of the page
    """
    questions = flatten(questions)
    return PageModel(name=name, questions=questions, **kwargs)


def dropdown(
    name: str, title: str | list[str] | None, *choices: str | dict | list, **kwargs
) -> QuestionDropdownModel | list[QuestionDropdownModel]:
    """Create a single-select dropdown question object

    Args:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        choices (str | dict | list): The choices for the question. Can be string(s) or dictionary(-ies) with structure `{"value": ..., "text": ...}`. You can also add `visibleIf`, `enableIf`, and `requiredIf` to the dictionary.
        choicesFromQuestion (str | None): The name of the question to get the choices from if the are to be copied. Use with `choicesFromQuestionMode`.
        choicesFromQuestionMode (str): The mode of copying choices. Can be 'all', 'selected', 'unselected'.
        choicesMax (int | None): Maximum for automatically generated choices. Use with `choicesMin` and `choicesStep`.
        choicesMin (int | None): Minimum for automatically generated choices. Use with `choicesMax` and `choicesStep`.
        choicesOrder (str): The order of the choices. Can be 'none', 'asc', 'desc', 'random'.
        choicesStep (int | None): Step for automatically generated choices. Use with `choicesMax` and `choicesMin`.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        dontKnowText: str | None = None
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideIfChoicesEmpty: bool | None = None
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        maxWidth (str): Maximum width of the question in CSS units.
        minWidth (str): Minimum width of the question in CSS units.
        noneText: str | None = None
        otherErrorText: str | None = None
        otherText: str | None = None
        placeholder (str | None): Placeholder text.
        readOnly (bool): Whether the question is read-only.
        refuseText: str | None = None
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showDontKnowItem: bool = False
        showNoneItem: bool = False
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        showOtherItem: bool = False
        showRefuseItem: bool = False
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.

    Returns:
        QuestionDropdownModel: The question object model or a list of question object models if `title` is a list.
    """
    choices = flatten(choices)
    if not isinstance(title, list):
        title = [title]
    if len(title) != 1:
        return [
            QuestionDropdownModel(
                name=f"{name}_{i+1}", title=t, choices=choices, **kwargs
            )
            for i, t in enumerate(title)
        ]
    else:
        return QuestionDropdownModel(
            name=name, title=title[0], choices=choices, **kwargs
        )


def text(name: str, *title: str | list[str] | None, **kwargs) -> QuestionTextModel:
    """Create a text question object

    Args:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        autocomplete (str | None): A value of `autocomplete` attribute for `<input>`. See MDN for a list: <https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete#token_list_tokens>.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        inputType (str | None): The type of the input. Can be 'text', 'password', 'email', 'url', 'tel', 'number', 'date', 'datetime-local', 'time', 'month', 'week', 'color'.
        max (str): The `max` attribute of `<input>`. Syntax depends on the `inputType`. See MDN for details: <https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/max>.
        maxErrorText (str | None): Error text if the value exceeds `max`.
        maxLength (int | None): The maximum length of the input in characters. Use 0 for no limit. Use -1 for the default limit.
        maxValueExpression (str | None): Expression to decide the maximum value.
        maxWidth (str): Maximum width of the question in CSS units.
        min (str | None): The `min` attribute of `<input>`. Syntax depends on the `inputType`. See MDN for details: <https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/min>.
        minErrorText (str | None): Error text if the value is less than `min`.
        minValueExpression (str | None): Expression to decide the minimum value.
        minWidth (str): Minimum width of the question in CSS units.
        placeholder (str | None): Placeholder text for the input.
        readOnly (bool): Whether the question is read-only.
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        size (int | None): The width of the input in characters. A value for `size` attribute of `<input>`.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        step (str | None): The `step` attribute of `<input>`. Syntax depends on the `inputType`. See MDN for details: <https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/step>.
        textUpdateMode (str): The mode of updating the text. Can be 'default', 'onBlur' (update after the field had been unclicked), 'onTyping' (update every key press).
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    title = flatten(title)
    if len(title) != 1:
        return [
            QuestionTextModel(name=f"{name}_{i+1}", title=t, **kwargs)
            for i, t in enumerate(title)
        ]
    return QuestionTextModel(name=name, title=title[0], **kwargs)


def checkbox(
    name: str, title: str | list[str] | None, *choices: str | dict | list, **kwargs
) -> QuestionCheckboxModel | list[QuestionCheckboxModel]:
    """Create a checkbox question object

    Args:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        choices (str | dict | list): The choices for the question. Can be string(s) or dictionary(-ies) with structure `{"value": ..., "text": ...}`. You can also add `visibleIf`, `enableIf`, and `requiredIf` to the dictionary.
        choicesFromQuestion (str | None): The name of the question to get the choices from if the are to be copied. Use with `choicesFromQuestionMode`.
        choicesFromQuestionMode (str): The mode of copying choices. Can be 'all', 'selected', 'unselected'.
        choicesOrder (str): The order of the choices. Can be 'none', 'asc', 'desc', 'random'.
        colCount (int | None): The number of columns for the choices. 0 means a single line.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        dontKnowText: str | None = None
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideIfChoicesEmpty: bool | None = None
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        isAllSelected (bool | None): Start with all choices selected. Default is False.
        maxSelectedChoices (int): Maximum number of selected choices. 0 means no limit.
        maxWidth (str): Maximum width of the question in CSS units.
        minSelectedChoices (int): Minimum number of selected choices. 0 means no limit.
        minWidth (str): Minimum width of the question in CSS units.
        noneText: str | None = None
        otherErrorText: str | None = None
        otherText: str | None = None
        readOnly (bool): Whether the question is read-only.
        refuseText: str | None = None
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        selectAllText (str | None): Text for the 'Select All' item.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showDontKnowItem: bool = False
        showNoneItem: bool = False
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        showOtherItem: bool = False
        showRefuseItem: bool = False
        showSelectAllItem (bool | None): Whether to show the 'Select All' item.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    choices = flatten(choices)
    if not isinstance(title, list):
        title = [title]
    if len(title) != 1:
        return [
            QuestionCheckboxModel(
                name=f"{name}_{i+1}", title=t, choices=choices, **kwargs
            )
            for i, t in enumerate(title)
        ]
    else:
        return QuestionCheckboxModel(
            name=name, title=title[0], choices=choices, **kwargs
        )


def ranking(
    name: str, title: str | list[str] | None, *choices: str | dict | list, **kwargs
):
    """Create a ranking question object

    Args:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        choices (str | dict | list): The choices for the question. Can be string(s) or dictionary(-ies) with structure `{"value": ..., "text": ...}`. You can also add `visibleIf`, `enableIf`, and `requiredIf` to the dictionary.
        choicesFromQuestion (str | None): The name of the question to get the choices from if the are to be copied. Use with `choicesFromQuestionMode`.
        choicesFromQuestionMode (str): The mode of copying choices. Can be 'all', 'selected', 'unselected'.
        choicesOrder (str): The order of the choices. Can be 'none', 'asc', 'desc', 'random'.
        colCount (int | None): The number of columns for the choices. 0 means a single line.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        dontKnowText: str | None = None
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideIfChoicesEmpty: bool | None = None
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        isAllSelected (bool | None): Start with all choices selected. Default is False.
        longTap (bool): Whether to use long tap for dragging on mobile devices.
        maxSelectedChoices (int): Maximum number of selected choices. 0 means no limit.
        maxWidth (str): Maximum width of the question in CSS units.
        minSelectedChoices (int): Minimum number of selected choices. 0 means no limit.
        minWidth (str): Minimum width of the question in CSS units.
        noneText: str | None = None
        otherErrorText: str | None = None
        otherText: str | None = None
        readOnly (bool): Whether the question is read-only.
        refuseText: str | None = None
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        selectAllText (str | None): Text for the 'Select All' item.
        selectToRankAreasLayout (str): The layout of the ranked and unranked areas when `selectToRankEnabled=True`. Can be 'horizontal', 'vertical'.
        selectToRankEmptyRankedAreaText (str | None): Text for the empty ranked area when `selectToRankEnabled=True`.
        selectToRankEmptyUnrankedAreaText (str | None): Text for the empty unranked area when `selectToRankEnabled=True`.
        selectToRankEnabled (bool): Whether user should select items they want to rank before ranking them. Default is False.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showDontKnowItem: bool = False
        showNoneItem: bool = False
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        showOtherItem: bool = False
        showRefuseItem: bool = False
        showSelectAllItem (bool | None): Whether to show the 'Select All' item.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    choices = flatten(choices)
    if not isinstance(title, list):
        title = [title]
    if len(title) != 1:
        return [
            QuestionRankingModel(
                name=f"{name}_{i+1}", title=t, choices=choices, **kwargs
            )
            for i, t in enumerate(title)
        ]
    else:
        return QuestionRankingModel(
            name=name, title=title[0], choices=choices, **kwargs
        )


def radio(
    name: str, title: str | list[str] | None, *choices: str | dict | list, **kwargs
) -> QuestionRadiogroupModel | list[QuestionRadiogroupModel]:
    """Create a radio question object

    Args:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        choices (str | dict | list): The choices for the question. Can be string(s) or dictionary(-ies) with structure `{"value": ..., "text": ...}`. You can also add `visibleIf`, `enableIf`, and `requiredIf` to the dictionary.
        choicesFromQuestion (str | None): The name of the question to get the choices from if the are to be copied. Use with `choicesFromQuestionMode`.
        choicesFromQuestionMode (str): The mode of copying choices. Can be 'all', 'selected', 'unselected'.
        choicesOrder (str): The order of the choices. Can be 'none', 'asc', 'desc', 'random'.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        colCount (int | None): The number of columns for the choices. 0 means a single line.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        dontKnowText: str | None = None
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideIfChoicesEmpty: bool | None = None
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        maxWidth (str): Maximum width of the question in CSS units.
        minWidth (str): Minimum width of the question in CSS units.
        noneText: str | None = None
        otherErrorText: str | None = None
        otherText: str | None = None
        readOnly (bool): Whether the question is read-only.
        refuseText: str | None = None
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showClearButton (bool): Show a button to clear the answer.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showDontKnowItem: bool = False
        showNoneItem: bool = False
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        showOtherItem: bool = False
        showRefuseItem: bool = False
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.

    Returns:
        QuestionRadiogroupModel: The question object model or a list of question object models if `title` is a list.
    """
    choices = flatten(choices)
    if not isinstance(title, list):
        title = [title]
    if len(title) != 1:
        return [
            QuestionRadiogroupModel(
                name=f"{name}_{i+1}", title=t, choices=choices, **kwargs
            )
            for i, t in enumerate(title)
        ]
    else:
        return QuestionRadiogroupModel(
            name=name, title=title[0], choices=choices, **kwargs
        )


def checkboxMultiple(
    name: str, title: str | list[str] | None, *choices: str | dict | list, **kwargs
):
    """Create a multiple checkbox question object

    Args:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        choices (str | dict | list): The choices for the question. Can be string(s) or dictionary(-ies) with structure `{"value": ..., "text": ...}`. You can also add `visibleIf`, `enableIf`, and `requiredIf` to the dictionary.
        allowClear (str): Whether to show the 'Clear' button for each answer.
        choicesFromQuestion (str | None): The name of the question to get the choices from if the are to be copied. Use with `choicesFromQuestionMode`.
        choicesFromQuestionMode (str): The mode of copying choices. Can be 'all', 'selected', 'unselected'.
        choicesOrder (str): The order of the choices. Can be 'none', 'asc', 'desc', 'random'.
        closeOnSelect (int | None): Whether to close the dropdown after user selects a specified number of items.
        colCount (int | None): The number of columns for the choices. 0 means a single line.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        dontKnowText: str | None = None
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideIfChoicesEmpty: bool | None = None
        hideNumber (bool): Whether to hide the question number.
        hideSelectedItems (bool | None): Whether to hide selected items in the dropdown.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        isAllSelected (bool | None): Start with all choices selected. Default is False.
        maxSelectedChoices (int): Maximum number of selected choices. 0 means no limit.
        maxWidth (str): Maximum width of the question in CSS units.
        minSelectedChoices (int): Minimum number of selected choices. 0 means no limit.
        minWidth (str): Minimum width of the question in CSS units.
        noneText: str | None = None
        otherErrorText: str | None = None
        otherText: str | None = None
        placeholder (str | None): Placeholder text for the input with no value.
        readOnly (bool): Whether the question is read-only.
        refuseText: str | None = None
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        searchEnabled (bool): Whether to enable search in the dropdown.
        searchMode (str): The search mode. Can be 'contains' (default), 'startsWith'. Works only if `searchEnabled=True`.
        selectAllText (str | None): Text for the 'Select All' item.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showDontKnowItem: bool = False
        showNoneItem: bool = False
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        showOtherItem: bool = False
        showRefuseItem: bool = False
        showSelectAllItem (bool | None): Whether to show the 'Select All' item.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    choices = flatten(choices)
    if not isinstance(title, list):
        title = [title]
    if len(title) != 1:
        return [
            QuestionTagboxModel(
                name=f"{name}_{i+1}", title=t, choices=choices, **kwargs
            )
            for i, t in enumerate(title)
        ]
    else:
        return QuestionTagboxModel(name=name, title=title[0], choices=choices, **kwargs)


def textLong(name: str, *title: str | list[str] | None, **kwargs):
    """Create a long text question object

    Attributes:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        acceptCarriageReturn (bool): Whether to allow line breaks. Default is True.
        allowResize (bool): Whether to allow resizing the input field. Default is True.
        autoGrow (bool): Whether to automatically grow the input field. Default is False.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        maxWidth (str): Maximum width of the question in CSS units.
        minWidth (str): Minimum width of the question in CSS units.
        readOnly (bool): Whether the question is read-only.
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        rows (int): Height of the input field in rows' number.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    title = flatten(title)
    if len(title) != 1:
        return [
            QuestionCommentModel(name=f"{name}_{i+1}", title=t, **kwargs)
            for i, t in enumerate(title)
        ]
    return QuestionCommentModel(name=name, title=title[0], **kwargs)


def rating(name: str, *title: str | list[str] | None, **kwargs):
    """Create a rating question object

    Attributes:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        maxRateDescription (str | None): Description for the biggest rate.
        maxWidth (str): Maximum width of the question in CSS units.
        minRateDescription (str | None): Description for the smallest rate.
        minWidth (str): Minimum width of the question in CSS units.
        rateMax (int): Maximum rate. Works only if `rateValues` is not set.
        rateMin (int): Minimum rate. Works only if `rateValues` is not set.
        rateStep (int): Step for the rate. Works only if `rateValues` is not set.
        rateType (str): The type of the rate. Can be 'labels', 'stars', 'smileys'.
        rateValues (list | None): Manually set rate values. Use a list of primitives and/or dictionaries `{"value": ..., "text": ...}`.
        readOnly (bool): Whether the question is read-only.
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        scaleColorMode (str): The color mode of the scale if `rateType='smileys'`. Can be 'monochrome', 'colored'.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    title = flatten(title)
    if len(title) != 1:
        return [
            QuestionRatingModel(name=f"{name}_{i+1}", title=t, **kwargs)
            for i, t in enumerate(title)
        ]
    return QuestionRatingModel(name=name, title=title[0], **kwargs)


def yesno(name: str, *title: str | list[str] | None, **kwargs):
    """Create a yes/no (boolean) question object

    Attributes:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        labelFalse (str | None): Label for the 'false' value.
        labelTrue (str | None): Label for the 'true' value.
        maxWidth (str): Maximum width of the question in CSS units.
        minWidth (str): Minimum width of the question in CSS units.
        readOnly (bool): Whether the question is read-only.
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        swapOrder (bool): Whether to swap the default (no, yes) order of the labels.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        valueFalse (str): Value for the 'false' option.
        valueTrue (str): Value for the 'true' option.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    title = flatten(title)
    if len(title) != 1:
        return [
            QuestionBooleanModel(name=f"{name}_{i+1}", title=t, **kwargs)
            for i, t in enumerate(title)
        ]
    return QuestionBooleanModel(name=name, title=title[0], **kwargs)


def info(name: str, *infoHTML: str | list[str], **kwargs):
    """Create an informational text object

    Args:
        name (str): The label of the question.
        infoHTML (str): The HTML content of the infobox.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        maxWidth (str): Maximum width of the question in CSS units.
        minWidth (str): Minimum width of the question in CSS units.
        readOnly (bool): Whether the question is read-only.
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        title (str | None): The visible title of the question. If None, `name` is used.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
    addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    infoHTML = flatten(infoHTML)
    if len(infoHTML) != 1:
        return [
            QuestionHtmlModel(name=f"{name}_{i+1}", html=html, **kwargs)
            for i, html in enumerate(infoHTML)
        ]
    return QuestionHtmlModel(name=name, html=infoHTML[0], **kwargs)


def matrix(name: str, title: str | list[str] | None, *columns, **kwargs):
    """Create a matrix question object

    Attributes:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        columns (list | dict): The columns of the matrix. Use primitives or dictionaries `{"text": ..., "value": ..., "type": ..., "otherParameter": ...}`.
        rows (list | dict): The rows of the matrix. Use primitives or dictionaries `{"text": ..., "value": ..., "otherParameter": ...}`.
        alternateRows (bool | None): Whether to alternate the rows.
        columnMinWidth (str | None): Minimum width of the column in CSS units.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        displayMode (str): The display mode of the matrix. Can be 'auto', 'list', 'table'.
        eachRowUnique (bool | None): Whether each row should have a unique answer. Defaults to False.
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideIfRowsEmpty (bool | None): Whether to hide the question if no rows are visible.
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        isAllRowRequired (bool): Whether each and every row is to be required.
        maxWidth (str): Maximum width of the question in CSS units.
        minWidth (str): Minimum width of the question in CSS units.
        readOnly (bool): Whether the question is read-only.
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        rowTitleWidth (str | None): Width of the row title in CSS units.
        rowsOrder (str): The order of the rows. Can be 'initial', 'random'.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showHeader (bool): Whether to show the header of the table.
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        verticalAlign (str): The vertical alignment of the content. Can be 'top', 'middle'.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    columns = flatten(columns)
    if not isinstance(title, list):
        title = [title]
    if len(title) != 1:
        return [
            QuestionMatrixModel(
                name=f"{name}_{i+1}", title=t, columns=columns, **kwargs
            )
            for i, t in enumerate(title)
        ]
    return QuestionMatrixModel(name=name, title=title[0], columns=columns, **kwargs)


def matrixDynamic(name: str, title: str | list[str] | None, *columns, **kwargs):
    """Create a dynamic matrix question object

    Attributes:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        columns (list | dict): The columns of the matrix. Use primitives or dictionaries `{"text": ..., "value": ..., "type": ..., "otherParameter": ...}`.
        rows (list | dict): The rows of the matrix. Use primitives or dictionaries `{"text": ..., "value": ..., "otherParameter": ...}`.
        addRowLocation (str): The location of the 'Add row' button. Can be 'default', 'top', 'bottom', 'topBottom' (both top and bottom).
        addRowText (str | None): Text for the 'Add row' button.
        allowAddRows (bool): Whether to allow adding rows.
        allowRemoveRows (bool): Whether to allow removing rows.
        allowRowsDragAndDrop (bool): Whether to allow dragging and dropping rows to change order.
        alternateRows (bool | None): Whether to alternate the rows.
        cellErrorLocation (str): The location of the error text for the cells. Can be 'default', 'top', 'bottom'.
        cellType (str | None): The type of the matrix cells. Can be overridden for individual columns. Can be "dropdown" (default), "checkbox", "radiogroup", "tagbox", "text", "comment", "boolean", "expression", "rating".
        choices (str | dict | list): The default choices for all select questions. Can be overridden for individual columns. Can be string(s) or dictionary(-ies) with structure `{"value": ..., "text": ..., "otherParameter": ...}`.
        columnMinWidth (str | None): Minimum width of the column in CSS units.
        columns (list | dict): The columns of the matrix. Use primitives or dictionaries `{"text": ..., "value": ..., "type": ..., "otherParameter": ...}`.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        confirmDelete (bool): Whether to prompt for confirmation before deleting a row. Default is False.
        confirmDeleteText (str | None): Text for the confirmation dialog when `confirmDelete` is True.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultRowValue (str | None): Default value for the new rows that has no `defaultValue` property.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        defaultValueFromLastRow (bool): Whether to copy the value from the last row to the new row.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        displayMode (str): The display mode of the matrix. Can be 'auto', 'list', 'table'.
        emptyRowsText (str | None): Text to display when there are no rows if `hideColumnsIfEmpty` is True.
        enableIf (str | None): Expression to enable the question.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideColumnsIfEmpty (bool): Whether to hide columns if there are no rows.
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        isUniqueCaseSensitive (bool): Whether the case of the answer should be considered when checking for uniqueness. If `True`, "Kowalski" and "kowalski" will be considered different answers.
        maxRowCount (int): Maximum number of rows.
        maxWidth (str): Maximum width of the question in CSS units.
        minRowCount (int): Minimum number of rows.
        minWidth (str): Minimum width of the question in CSS units.
        placeHolder (str | None): Placeholder text for the cells.
        readOnly (bool): Whether the question is read-only.
        removeRowText (str | None): Text for the 'Remove row' button.
        required (bool): Whether the question is required.
        requiredErrorText (str | None): Error text if the required condition is not met.
        requiredIf (str | None): Expression to make the question required.
        resetValueIf (str | None): Expression to reset the value of the question.
        rowCount (int): The initial number of rows.
        rowTitleWidth (str | None): Width of the row title in CSS units.
        rows (list | dict): The rows of the matrix. Use primitives or dictionaries `{"text": ..., "value": ...}`.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        showHeader (bool): Whether to show the header of the table.
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        transposeData (bool): Whether to show columns as rows. Default is False.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        verticalAlign (str): The vertical alignment of the content. Can be 'top', 'middle'.
        visible (bool): Whether the question is visible.
        visibleIf (str | None): Expression to make the question visible.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    columns = flatten(columns)
    if not isinstance(title, list):
        title = [title]
    if len(title) != 1:
        return [
            QuestionMatrixDynamicModel(
                name=f"{name}_{i+1}", title=t, columns=columns, **kwargs
            )
            for i, t in enumerate(title)
        ]
    return QuestionMatrixDynamicModel(
        name=name, title=title[0], columns=columns, **kwargs
    )


def slider(name: str, *title: str | list[str] | None, **kwargs):
    """Create a slider question object

    Args:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        step (int): The step of the slider.
        rangeMin (int): The minimum value of the slider.
        rangeMax (int): The maximum value of the slider.
        pipsMode (str): The mode of the pips. Can be 'positions', 'values', 'count', 'range', 'steps'. See <https://refreshless.com/nouislider/pips/>
        pipsValues (list): The values of the pips.
        pipsText (list): The text of the pips.
        pipsDensity (int): The density of the pips.
        orientation (str): The orientation of the slider. Can be 'horizontal', 'vertical'.
        direction (str): The direction of the slider. Can be 'ltr', 'rtl'.
        tooltips (bool): Whether to show tooltips.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """
    title = flatten(title)
    if len(title) != 1:
        return [
            QuestionNoUiSliderModel(name=f"{name}_{i+1}", title=t, **kwargs)
            for i, t in enumerate(title)
        ]
    return QuestionNoUiSliderModel(name=name, title=title[0], **kwargs)
