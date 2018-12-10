package com.natejschmidt.autoassistant.actions

import com.natejschmidt.autoassistant.com.natejschmidt.autoassistant.models.RandomMinMaxXYClickModel
import com.natejschmidt.autoassistant.main.AutomatedProcessView
import javafx.beans.property.SimpleStringProperty
import javafx.event.EventHandler
import javafx.scene.Parent
import javafx.scene.control.Button
import javafx.scene.input.KeyEvent
import javafx.scene.text.Font
import tornadofx.*
import java.awt.MouseInfo
import java.awt.Robot
import java.awt.event.InputEvent
import kotlin.random.Random

class RandomMinMaxXYClickController(private val model: RandomMinMaxXYClickModel) : Action() {

    val myRobot = Robot()

    override fun getType(): ActionType {
        return ActionType.RANDOM_MIN_MAX_X_Y_CLICK
    }

    override fun execute() {
        val origX = MouseInfo.getPointerInfo().location.x
        val origY = MouseInfo.getPointerInfo().location.y

        myRobot.mouseMove(Random.nextInt(model.theXMin, model.theXMax + 1), Random.nextInt(model.theYMin, model.theYMax + 1))
        myRobot.mousePress(InputEvent.BUTTON1_MASK)
        myRobot.mouseRelease(InputEvent.BUTTON1_MASK)
        myRobot.mouseMove(origX, origY)
    }
}

class CreateRandomMinMaxXYClickView : Fragment() {
    //model
    val actionList: MutableList<Action> by param()

    //view stuff
    override val root = form {
        form {
            fieldset("Click form") {
                button("Create action") {
                    action {
//                        openInternalWindow(
//                                find<CaptureKeyPressView>(mapOf(CaptureKeyPressView::actionList to actionList)),
//                                owner = parent)
                        replaceWith(find<CaptureKeyPressView>(mapOf(CaptureKeyPressView::actionList to actionList)))
                    }
                }
            }
        }
    }

//    fun switchStuff() {
//        root.parent.replaceWith(find<CaptureKeyPressView>(mapOf(CaptureKeyPressView::actionList to actionList)))
//    }
}

class CaptureKeyPressView : View() {
    //model stuff
    val actionList: MutableList<Action> by param()

    //controller stuff
    private var clickCounter = 0
    private var click1X = -1
    private var click1Y = -1
    private var click2X = -1
    private var click2Y = -1

    //view stuff
    private val firstClickRecord = SimpleStringProperty("waiting for button click")
    private var secondClickRecord = SimpleStringProperty("waiting for button click")

    private val keyEventHandler = EventHandler<KeyEvent> {
        when (clickCounter) {
            0 -> {
                println("clicked once:  ${it.character}")
                click1X = MouseInfo.getPointerInfo().location.x
                click1Y = MouseInfo.getPointerInfo().location.y
                firstClickRecord.value = "($click1X, $click1Y)"
            }
            1 -> {
                println("clicked twice: ${it.character}")
                click2X = MouseInfo.getPointerInfo().location.x
                click2Y = MouseInfo.getPointerInfo().location.y
                secondClickRecord.value = "($click2X, $click2Y)"

                //update the model with the new action
//                val index = actionList.size
//                val randomMinMaxXYClickModel = RandomMinMaxXYClickModel(index, click1X, click2X, click1Y, click2Y)
//                actionList.add(RandomMinMaxXYClickController(randomMinMaxXYClickModel))
                switchViewToCaptureKeyPressView()

//                replaceWith(find<AutomatedProcessView>(mapOf(AutomatedProcessView::actionList to actionList)))
            }
            else -> println("Oh dear, it didn't get removed")
        }
        clickCounter++
    }

    private fun switchViewToCaptureKeyPressView() {
        replaceWith(find<ConfirmKeysPressed>(mapOf(
                ConfirmKeysPressed::actionList to actionList,
                ConfirmKeysPressed::click1X to click1X,
                ConfirmKeysPressed::click1Y to click1Y,
                ConfirmKeysPressed::click2X to click2X,
                ConfirmKeysPressed::click2Y to click2Y,
                ConfirmKeysPressed::keyEventHandler to keyEventHandler
        )))
    }

    override val root = vbox {
        label {
            text = "Capturing key presses"
            font = Font.font(32.0)
        }
        hbox {
            label("First key click:  ")
            label(firstClickRecord)
        }
        hbox {
            label("Second key click: ")
            label(secondClickRecord)
        }
        primaryStage.addEventHandler(KeyEvent.KEY_TYPED, keyEventHandler)
    }
}

class ConfirmKeysPressed : View() {
    val actionList: MutableList<Action> by param()
    val keyEventHandler: EventHandler<KeyEvent> by param()
    val click1X: Int by param()
    val click1Y: Int by param()
    val click2X: Int by param()
    val click2Y: Int by param()

    override val root = vbox {
        // remove the event handler from the previous view
        primaryStage.removeEventHandler(KeyEvent.KEY_TYPED, keyEventHandler)

        label {
            text = "Confirm locations of keys pressed"
            font = Font.font(36.0)
        }
        label("First key click:  ($click1X, $click1Y)")
        label("Second key click: ($click2X, $click2Y)")
        hbox {
            button("Confirm") {
                action {
                    val index = actionList.size
                    val randomMinMaxXYClickModel = RandomMinMaxXYClickModel(index, click1X, click2X, click1Y, click2Y)
                    actionList.add(RandomMinMaxXYClickController(randomMinMaxXYClickModel))
                    replaceWith(find<AutomatedProcessView>(mapOf(AutomatedProcessView::actionList to actionList)))
                }
            }
            button("Cancel") {
                action {

                }
            }
        }

    }
}