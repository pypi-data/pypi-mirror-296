"""Classes for basic structural elements for SurveyJS"""

import json
import os
import shutil
from pathlib import Path
from importlib.resources import files
from markdown import markdown
from pydantic import BaseModel
from pynpm import YarnPackage
from .validators import ValidatorModel
from .utils import dict_without_defaults


class QuestionModel(BaseModel):
    """General question object model

    Attributes:
        name (str): The label of the question.
        title (str | None): The visible title of the question. If None, `name` is used.
        titleLocation (str): The location of the title. Can be 'default', 'top', 'bottom', 'left', 'hidden'.
        description (str | None): Optional subtitle or description of the question.
        descriptionLocation (str): The location of the description. Can be 'default', 'underTitle', 'underInput'.
        isRequired (bool): Whether the question is required.
        readOnly (bool): Whether the question is read-only.
        visible (bool): Whether the question is visible.
        requiredIf (str | None): Expression to make the question required.
        enableIf (str | None): Expression to enable the question.
        visibleIf (str | None): Expression to make the question visible.
        validators (ValidatorModel | list[ValidatorModel] | None): Validator(s) for the question.
        showOtherItem (bool): Whether to show the 'Other' item. Doesn't work with `showCommentArea`.
        showCommentArea (bool): Whether to show the comment area. Doesn't work with `showOtherItem`.
        commentPlaceholder (str | None): Placeholder text for the comment area.
        commentText (str | None): Text for the comment area.
        correctAnswer (str | None): Correct answer for the question. Use for quizzes.
        defaultValue (str | None): Default value for the question.
        defaultValueExpression (str | None): Expression deciding the default value for the question.
        requiredErrorText (str | None): Error text if the required condition is not met.
        errorLocation (str | None): Location of the error text. Can be 'default' 'top', 'bottom'.
        hideNumber (bool): Whether to hide the question number.
        id (str | None): HTML id attribute for the question. Usually not necessary.
        maxWidth (str): Maximum width of the question in CSS units.
        minWidth (str): Minimum width of the question in CSS units.
        resetValueIf (str | None): Expression to reset the value of the question.
        setValueIf (str | None): Expression with a condition to set the value of the question. Requires `setValueExpression`.
        setValueExpression (str | None): Expression to decide on the value of the question to be set. Requires `setValueIf`.
        startWithNewLine (bool): Whether to start the question on a new line.
        state (str | None): If the question should be collapsed or expanded. Can be 'default', 'collapsed', 'expanded'.
        useDisplayValuesInDynamicTexts (bool): Whether to use display names for question values in placeholders.
        width (str): Width of the question in CSS units.
        addCode (dict | None): Additional code for the question. Usually not necessary.
    """

    name: str
    title: str | None
    type: str
    titleLocation: str = "default"
    description: str | None = None
    descriptionLocation: str = "default"
    isRequired: bool = False
    readOnly: bool = False
    visible: bool = True
    requiredIf: str | None = None
    enableIf: str | None = None
    visibleIf: str | None = None
    validators: ValidatorModel | list[ValidatorModel] | None = None
    showOtherItem: bool = False
    showCommentArea: bool = False
    commentPlaceholder: str | None = None
    commentText: str | None = None
    correctAnswer: str | None = None
    defaultValue: str | None = None
    defaultValueExpression: str | None = None
    requiredErrorText: str | None = None
    errorLocation: str = "default"
    hideNumber: bool = False
    id: str | None = None
    maxWidth: str = "100%"
    minWidth: str = "300px"
    resetValueIf: str | None = None
    setValueIf: str | None = None
    setValueExpression: str | None = None
    startWithNewLine: bool = True
    state: str = "default"
    useDisplayValuesInDynamicTexts: bool = True
    width: str = ""
    addCode: dict | None = None

    def __str__(self) -> str:
        return f"  {self.name} ({self.type}): {self.title}"

    def dict(self) -> dict:
        if self.validators is not None:
            if isinstance(self.validators, list):
                validators = {
                    "validators": [validator.dict() for validator in self.validators]
                }
            else:
                validators = {"validators": [self.validators.dict()]}
        else:
            validators = {}

        if self.addCode is not None:
            addCode = self.addCode
        else:
            addCode = {}
        return dict_without_defaults(self) | validators | addCode


class QuestionSelectBase(QuestionModel):
    """Base class for select type question object models

    Attributes:
        choices (str | dict | list): The choices for the question. Can be string(s) or dictionary(-ies) with structure `{"value": ..., "text": ...}`. You can also add `visibleIf`, `enableIf`, and `requiredIf` to the dictionary.
        choicesFromQuestion (str | None): The name of the question to get the choices from if the are to be copied. Use with `choicesFromQuestionMode`.
        choicesFromQuestionMode (str): The mode of copying choices. Can be 'all', 'selected', 'unselected'.
        choicesOrder (str): The order of the choices. Can be 'none', 'asc', 'desc', 'random'.
        showDontKnowItem: bool = False
        dontKnowText: str | None = None
        hideIfChoicesEmpty: bool | None = None
        showNoneItem: bool = False
        noneText: str | None = None
        showOtherItem: bool = False
        otherText: str | None = None
        otherErrorText: str | None = None
        showRefuseItem: bool = False
        refuseText: str | None = None
    """

    choices: str | dict | list
    choicesFromQuestion: str | None = None
    choicesFromQuestionMode: str = "all"
    choicesOrder: str = "none"
    showDontKnowItem: bool = False
    dontKnowText: str | None = None
    hideIfChoicesEmpty: bool | None = None
    showNoneItem: bool = False
    noneText: str | None = None
    showOtherItem: bool = False
    otherText: str | None = None
    otherErrorText: str | None = None
    showRefuseItem: bool = False
    refuseText: str | None = None


class QuestionDropdownModel(QuestionSelectBase):
    """A dropdown type question object model

    Attributes:
        choicesMax (int | None): Maximum for automatically generated choices. Use with `choicesMin` and `choicesStep`.
        choicesMin (int | None): Minimum for automatically generated choices. Use with `choicesMax` and `choicesStep`.
        choicesStep (int | None): Step for automatically generated choices. Use with `choicesMax` and `choicesMin`.
        placeholder (str | None): Placeholder text.
    """

    choicesMax: int | None = None
    choicesMin: int | None = None
    choicesStep: int | None = None
    placeholder: str | None = None

    def __init__(self, **kwargs):
        super().__init__(type="dropdown", **kwargs)


class QuestionTextModel(QuestionModel):
    """A short text type question object model

    Attributes:
        autocomplete (str | None): A value of `autocomplete` attribute for `<input>`. See MDN for a list: <https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete#token_list_tokens>.
        inputType (str | None): The type of the input. Can be 'text', 'password', 'email', 'url', 'tel', 'number', 'date', 'datetime-local', 'time', 'month', 'week', 'color'.
        max (str): The `max` attribute of `<input>`. Syntax depends on the `inputType`. See MDN for details: <https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/max>.
        maxErrorText (str | None): Error text if the value exceeds `max`.
        maxLength (int | None): The maximum length of the input in characters. Use 0 for no limit. Use -1 for the default limit.
        maxValueExpression (str | None): Expression to decide the maximum value.
        min (str | int | None): The `min` attribute of `<input>`. Syntax depends on the `inputType`. See MDN for details: <https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/min>.
        minErrorText (str | None): Error text if the value is less than `min`.
        minValueExpression (str | None): Expression to decide the minimum value.
        placeholder (str | None): Placeholder text for the input.
        size (int | None): The width of the input in characters. A value for `size` attribute of `<input>`.
        step (str | None): The `step` attribute of `<input>`. Syntax depends on the `inputType`. See MDN for details: <https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/step>.
        textUpdateMode (str): The mode of updating the text. Can be 'default', 'onBlur' (update after the field had been unclicked), 'onTyping' (update every key press).
    """

    autocomplete: str | None = None
    inputType: str = "text"
    max: str | None = None
    maxErrorText: str | None = None
    maxLength: int | None = None
    maxValueExpression: str | None = None
    min: str | int | None = None
    minErrorText: str | None = None
    minValueExpression: str | None = None
    placeholder: str | None = None
    size: int | None = None
    step: str | None = None
    textUpdateMode: str = "default"

    def __init__(self, **kwargs):
        super().__init__(type="text", **kwargs)


class QuestionCheckboxBase(QuestionSelectBase):
    """Base class for checkbox type question object models

    Attributes:
        colCount (int | None): The number of columns for the choices. 0 means a single line.
    """

    colCount: int | None = None


class QuestionCheckboxModel(QuestionCheckboxBase):
    """A checkbox type question object model

    Attributes:
        isAllSelected (bool | None): Start with all choices selected. Default is False.
        maxSelectedChoices (int): Maximum number of selected choices. 0 means no limit.
        minSelectedChoices (int): Minimum number of selected choices. 0 means no limit.
        selectAllText (str | None): Text for the 'Select All' item.
        showSelectAllItem (bool | None): Whether to show the 'Select All' item.
    """

    isAllSelected: bool | None = None
    maxSelectedChoices: int = 0
    minSelectedChoices: int = 0
    selectAllText: str | None = None
    showSelectAllItem: bool | None = None

    def __init__(self, **kwargs):
        super().__init__(type="checkbox", **kwargs)


class QuestionRankingModel(QuestionCheckboxModel):
    """A ranking type question object model

    Attributes:
        longTap (bool): Whether to use long tap for dragging on mobile devices.
        selectToRankAreasLayout (str): The layout of the ranked and unranked areas when `selectToRankEnabled=True`. Can be 'horizontal', 'vertical'.
        selectToRankEmptyRankedAreaText (str | None): Text for the empty ranked area when `selectToRankEnabled=True`.
        selectToRankEmptyUnrankedAreaText (str | None): Text for the empty unranked area when `selectToRankEnabled=True`.
        selectToRankEnabled (bool): Whether user should select items they want to rank before ranking them. Default is False.
    """

    longTap: bool = True
    selectToRankAreasLayout: str = "horizontal"
    selectToRankEmptyRankedAreaText: str | None = None
    selectToRankEmptyUnrankedAreaText: str | None = None
    selectToRankEnabled: bool = False

    def __init__(self, **kwargs):
        super().__init__(type="ranking", **kwargs)


class QuestionRadiogroupModel(QuestionCheckboxBase):
    """A radiogroup type question object model

    Attributes:
        showClearButton (bool): Show a button to clear the answer.
    """

    showClearButton: bool = False

    def __init__(self, **kwargs):
        super().__init__(type="radiogroup", **kwargs)

    def __str__(self):
        string = super().__str__() + "\n"
        for i, choice in enumerate(self.choices):
            string += f"    {i + 1}. {choice}\n"
        return string


class QuestionTagboxModel(QuestionCheckboxModel):
    """A multiselect dropdown type question object model

    Attributes:
        allowClear (str): Whether to show the 'Clear' button for each answer.
        closeOnSelect (int | None): Whether to close the dropdown after user selects a specified number of items.
        hideSelectedItems (bool | None): Whether to hide selected items in the dropdown.
        placeholder (str | None): Placeholder text for the input with no value.
        searchEnabled (bool): Whether to enable search in the dropdown.
        searchMode (str): The search mode. Can be 'contains' (default), 'startsWith'. Works only if `searchEnabled=True`.
    """

    allowClear: bool = True
    closeOnSelect: int | None = None
    hideSelectedItems: bool | None = False
    placeholder: str | None = None
    searchEnabled: bool = True
    searchMode: str = "contains"

    def __init__(self, **kwargs):
        super().__init__(type="tagbox", **kwargs)


class QuestionCommentModel(QuestionModel):
    """A long text type question object model

    Attributes:
        acceptCarriageReturn (bool): Whether to allow line breaks. Default is True.
        allowResize (bool): Whether to allow resizing the input field. Default is True.
        autoGrow (bool): Whether to automatically grow the input field. Default is False.
        rows (int): Height of the input field in rows' number.
    """

    acceptCarriageReturn: bool = True
    allowResize: bool | None = None
    autoGrow: bool | None = None
    rows: int = 4

    def __init__(self, **kwargs):
        super().__init__(type="comment", **kwargs)


class QuestionRatingModel(QuestionModel):
    """A rating type question object model

    Attributes:
        maxRateDescription (str | None): Description for the biggest rate.
        minRateDescription (str | None): Description for the smallest rate.
        rateMax (int): Maximum rate. Works only if `rateValues` is not set.
        rateMin (int): Minimum rate. Works only if `rateValues` is not set.
        rateStep (int): Step for the rate. Works only if `rateValues` is not set.
        rateType (str): The type of the rate. Can be 'labels', 'stars', 'smileys'.
        rateValues (list | None): Manually set rate values. Use a list of primitives and/or dictionaries `{"value": ..., "text": ...}`.
        scaleColorMode (str): The color mode of the scale if `rateType='smileys'`. Can be 'monochrome', 'colored'.
    """

    maxRateDescription: str | None = None
    minRateDescription: str | None = None
    rateMax: int = 5
    rateMin: int = 1
    rateStep: int = 1
    rateType: str = "labels"
    rateValues: list | None = None
    scaleColorMode: str = "monochrome"

    def __init__(self, **kwargs):
        super().__init__(type="rating", **kwargs)


class QuestionImagePickerModel(QuestionModel):
    """An image picker type question object model"""

    def __init__(self, **kwargs):
        super().__init__(type="imagepicker", **kwargs)

    # TODO


class QuestionBooleanModel(QuestionModel):
    """A yes/no type question object model

    Attributes:
        labelFalse (str | None): Label for the 'false' value.
        labelTrue (str | None): Label for the 'true' value.
        swapOrder (bool): Whether to swap the default (no, yes) order of the labels.
        valueFalse (str): Value for the 'false' option.
        valueTrue (str): Value for the 'true' option.
    """

    labelFalse: str | None = None
    labelTrue: str | None = None
    swapOrder: bool = False
    valueFalse: bool | str = False
    valueTrue: bool | str = True

    def __init__(self, **kwargs):
        super().__init__(type="boolean", **kwargs)


class QuestionImageModel(QuestionModel):
    """An image type question object model"""

    def __init__(self, **kwargs):
        super().__init__(type="image", **kwargs)

    # TODO


class QuestionHtmlModel(QuestionModel):
    """An info type question object model

    Attributes:
        html (str): The HTML content of the infobox.
    """

    html: str

    def __init__(self, **kwargs):
        super().__init__(type="html", title=None, **kwargs)
        self.html = markdown(self.html)

    def __str__(self):
        return f"  {self.name} ({self.type}): {self.html[:20]}…\n"


class QuestionSignaturePadModel(QuestionModel):
    """A signature pad type question object model"""

    def __init__(self, **kwargs):
        super().__init__(type="signaturepad", **kwargs)

    # TODO


class QuestionExpressionModel(QuestionModel):
    """An expression type question object model (read-only)"""

    def __init__(self, **kwargs):
        super().__init__(type="expression", **kwargs)

    # TODO


class QuestionFileModel(QuestionModel):
    """A file type question object model"""

    def __init__(self, **kwargs):
        super().__init__(type="file", **kwargs)

    # TODO


class QuestionMatrixBaseModel(QuestionModel):
    """Base for matrix type questions

    Attributes:
        columns (list | dict): The columns of the matrix. Use primitives or dictionaries `{"text": ..., "value": ..., "type": ..., "otherParameter": ...}`.
        rows (list | dict | None): The rows of the matrix. Use primitives or dictionaries `{"text": ..., "value": ...}`.
        alternateRows (bool | None): Whether to alternate the rows.
        columnMinWidth (str | None): Minimum width of the column in CSS units.
        displayMode (str): The display mode of the matrix. Can be 'auto', 'list', 'table'.
        rowTitleWidth (str | None): Width of the row title in CSS units.
        showHeader (bool): Whether to show the header of the table.
        verticalAlign (str): The vertical alignment of the content. Can be 'top', 'middle'.
    """

    columns: list | dict
    rows: list | dict | None = None
    alternateRows: bool | None = None
    columnMinWidth: str | None = None
    displayMode: str = "auto"
    rowTitleWidth: str | None = None
    showHeader: bool = True
    verticalAlign: str = "middle"

    def dict(self):
        if self.columns is not None:
            columns = {
                "columns": [
                    column.dict() if not isinstance(column, dict) else column
                    for column in self.columns
                ]
            }
            for col in columns["columns"]:
                if "type" in col:
                    col["cellType"] = col.pop("type")
        else:
            columns = {}

        if self.validators is not None:
            if isinstance(self.validators, list):
                validators = {
                    "validators": [validator.dict() for validator in self.validators]
                }
            else:
                validators = {"validators": [self.validators.dict()]}
        else:
            validators = {}

        if self.addCode is not None:
            addCode = self.addCode
        else:
            addCode = {}

        return dict_without_defaults(self) | columns | validators | addCode


class QuestionMatrixDropdownModelBase(QuestionMatrixBaseModel):
    """Base for matrix dropdown type questions

    Attributes:
        cellErrorLocation (str): The location of the error text for the cells. Can be 'default', 'top', 'bottom'.
        cellType (str | None): The type of the matrix cells. Can be overridden for individual columns. Can be "dropdown" (default), "checkbox", "radiogroup", "tagbox", "text", "comment", "boolean", "expression", "rating".
        choices (str | dict | list | None): The default choices for all select questions. Can be overridden for individual columns. Can be string(s) or dictionary(-ies) with structure `{"value": ..., "text": ..., "otherParameter": ...}`.
        isUniqueCaseSensitive (bool): Whether the case of the answer should be considered when checking for uniqueness. If `True`, "Kowalski" and "kowalski" will be considered different answers.
        placeHolder (str | None): Placeholder text for the cells.
        transposeData (bool): Whether to show columns as rows. Default is False.
    """

    cellErrorLocation: str = "default"
    cellType: str | None = None
    choices: str | dict | list | None = None
    isUniqueCaseSensitive: bool = False
    placeHolder: str | None = None
    transposeData: bool = False


class QuestionMatrixModel(QuestionMatrixBaseModel):
    """A single-select matrix type question object model

    Attributes:
        eachRowUnique (bool | None): Whether each row should have a unique answer. Defaults to False.
        hideIfRowsEmpty (bool | None): Whether to hide the question if no rows are visible.
        isAllRowRequired (bool): Whether each and every row is to be required.
        rowsOrder (str): The order of the rows. Can be 'initial', 'random'.
    """

    eachRowUnique: bool | None = None
    hideIfRowsEmpty: bool | None = None
    isAllRowRequired: bool = False
    rowsOrder: str = "initial"

    def __init__(self, **kwargs):
        super().__init__(type="matrix", **kwargs)


class QuestionMatrixDropdownModel(QuestionModel):
    """A multi-select matrix type question object model"""

    def __init__(self, **kwargs):
        super().__init__(type="matrixdropdown", **kwargs)

    # TODO


class QuestionMatrixDynamicModel(QuestionMatrixDropdownModelBase):
    """A dynamic matrix type question object model

    Attributes:
        addRowLocation (str): The location of the 'Add row' button. Can be 'default', 'top', 'bottom', 'topBottom' (both top and bottom).
        addRowText (str | None): Text for the 'Add row' button.
        allowAddRows (bool): Whether to allow adding rows.
        allowRemoveRows (bool): Whether to allow removing rows.
        allowRowsDragAndDrop (bool): Whether to allow dragging and dropping rows to change order.
        confirmDelete (bool): Whether to prompt for confirmation before deleting a row. Default is False.
        confirmDeleteText (str | None): Text for the confirmation dialog when `confirmDelete` is True.
        defaultRowValue (str | None): Default value for the new rows that has no `defaultValue` property.
        defaultValueFromLastRow (bool): Whether to copy the value from the last row to the new row.
        emptyRowsText (str | None): Text to display when there are no rows if `hideColumnsIfEmpty` is True.
        hideColumnsIfEmpty (bool): Whether to hide columns if there are no rows.
        maxRowCount (int): Maximum number of rows.
        minRowCount (int): Minimum number of rows.
        removeRowText (str | None): Text for the 'Remove row' button.
        rowCount (int): The initial number of rows.
    """

    addRowLocation: str = "default"
    addRowText: str | None = None
    allowAddRows: bool = True
    allowRemoveRows: bool = True
    allowRowsDragAndDrop: bool = False
    confirmDelete: bool = False
    confirmDeleteText: str | None = None
    defaultRowValue: str | None = None
    defaultValueFromLastRow: bool = False
    emptyRowsText: str | None = None
    hideColumnsIfEmpty: bool = False
    maxRowCount: int = 1000
    minRowCount: int = 0
    removeRowText: str | None = None
    rowCount: int = 2

    def __init__(self, **kwargs):
        super().__init__(type="matrixdynamic", **kwargs)


class QuestionMultipleTextModel(QuestionModel):
    """A multiple text type question object model"""

    def __init__(self, **kwargs):
        super().__init__(type="multipletext", **kwargs)

    # TODO


class QuestionNoUiSliderModel(QuestionModel):
    """A noUiSlider type question object model

    Attributes:
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
    """

    step: int = 1
    rangeMin: int = 0
    rangeMax: int = 100
    pipsMode: str = "positions"
    pipsValues: list = [0, 25, 50, 75, 100]
    pipsText: list = [0, 25, 50, 75, 100]
    pipsDensity: int = 5
    orientation: str = "horizontal"
    direction: str = "ltr"
    tooltips: bool = True

    def __init__(self, **kwargs):
        super().__init__(type="nouislider", **kwargs)


class PageModel(BaseModel):
    """Object model for page data

    Attributes:
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
        addCode (dict | None): Additional code for the page. Usually not necessary.
    """

    name: str
    questions: QuestionModel | list
    description: str | None = None
    enableIf: str | None = None
    id: str | None = None
    isRequired: bool = False
    maxTimeToFinish: int | None = None
    maxWidth: str = "100%"
    minWidth: str = "300px"
    navigationButtonsVisibility: str = "inherit"
    navigationDescription: str | None = None
    navigationTitle: str | None = None
    questionErrorLocation: str = "default"
    questionTitleLocation: str = "default"
    questionsOrder: str = "default"
    readOnly: bool = False
    requiredErrorText: str | None = None
    requiredIf: str | None = None
    state: str = "default"
    title: str | None = None
    visible: bool = True
    visibleIf: str | None = None
    visibleIndex: int | None = None
    addCode: dict | None = None

    def __str__(self) -> str:
        return f"Page: {self.name}\n" + "\n".join(
            [str(question) for question in self.questions]
        )

    def dict(self) -> dict:
        return dict_without_defaults(self) | {
            "elements": [question.dict() for question in self.questions]
        }


class SurveyModel(BaseModel):
    """Object model for survey data

    Attributes:
        pages (list[PageModel]): The pages of the survey.
        title (str | None): The title of the survey.
        html (str | None): The HTML content to show after the survey is completed.
        locale (str): The locale of the survey. Default is 'en'.
        firstPageIsStarted (bool): Whether the first page is a start page.
        addCode (dict | None): Additional code for the survey. Usually not necessary.
    """

    pages: list[PageModel]
    title: str | None = None
    html: str | None = None
    locale: str = "en"
    numberOfGroups: int = 1
    firstPageIsStarted: bool = False
    addCode: dict | None = None

    def __str__(self) -> str:
        first_line = "VelesSurvey" + (f' ("{self.title}")\n' if self.title else "\n")
        return (
            first_line
            + "-" * (len(first_line) - 1)
            + "\n"
            + "\n".join([str(page) for page in self.pages])
            + "-" * (len(first_line) - 1)
        )

    def dict(self) -> dict:
        return dict_without_defaults(self) | {
            "pages": [page.dict() for page in self.pages]
        }

    def json(self) -> str:
        return json.dumps(self.dict())

    def createStructure(
        self, path: str | Path = os.getcwd(), folderName: str = "survey"
    ):
        """Create the file structure for the survey but not build it"""

        if isinstance(path, str):
            path = Path(path)

        path = path / folderName

        # main file structure
        if not os.path.exists(path / "package.json"):
            template = str(files("velesresearch.website_template"))
            shutil.copytree(
                template,
                path,
                ignore=shutil.ignore_patterns("__pycache__", "__init__.py"),
            )

        # do Yarn stuff if needed
        if not os.path.exists(path / "node_modules"):
            YarnPackage(path).install()

        # survey.js
        with open(path / "src" / "survey.js", "w", encoding="utf-8") as survey_js:
            survey_js.write("export const json = " + self.json() + ";")

        # config.js
        shutil.copyfile(
            files("velesresearch.website_template") / "src" / "config.js",
            path / "src" / "config.js",
        )
        with open(path / "src" / "config.js", "r", encoding="utf-8") as configJS:
            configJSData = configJS.read()

            # number of groups
            configJSData = configJSData.replace(
                r"{% numberOfGroups %}", str(self.numberOfGroups)
            )
        with open(path / "src" / "config.js", "w", encoding="utf-8") as configJS:
            configJS.write(configJSData)

    def buildForProduction(
        self, path: str | Path = os.getcwd(), folderName: str = "survey"
    ):
        """Update the survey and build it for production"""
        if isinstance(path, str):
            path = Path(path)

        self.createStructure(path, folderName)

        YarnPackage(path / folderName)._run_npm("build")
