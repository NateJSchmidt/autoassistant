package com.natejschmidt.autoassistant.main

import com.natejschmidt.autoassistant.actions.Action
import com.natejschmidt.autoassistant.actions.ActionType
import com.natejschmidt.autoassistant.actions.CreateRandomMinMaxWaitView
import com.natejschmidt.autoassistant.actions.CreateRandomMinMaxXYClickView
import javafx.application.Platform
import javafx.beans.property.SimpleObjectProperty
import javafx.collections.FXCollections
import javafx.event.EventHandler
import javafx.scene.control.Button
import javafx.scene.input.KeyEvent
import tornadofx.*
import java.awt.MouseInfo

class AutomatedProcessView : View("Create Process") {
    val actionList: MutableList<Action> by param()

    override fun onDock() {
        super.onDock()
        println("ActionList size is ${actionList.size}")
    }

    override val root = borderpane {
        left = vbox {
            val mutableListOfActionTypes = mutableListOf<ActionType>()
            ActionType.values().forEach { mutableListOfActionTypes.add(it) }

            val actionTypes = FXCollections.observableArrayList(mutableListOfActionTypes)
            val selectedActionType = SimpleObjectProperty<ActionType>()

            combobox(selectedActionType, actionTypes)
            selectedActionType.onChange {
                println("new item selected: $it : [${it?.name}]")
                left.getChildList()?.removeIf {
                    it is Form
                }
                if (it?.name != null) {
                    val selected = ActionType.valueOf(it.name)
                    when (selected) {
                        // TODO - there is a bug here when switching back and forth...not sure why...
                        ActionType.RANDOM_MIN_MAX_X_Y_CLICK -> {
                            this += find<CreateRandomMinMaxXYClickView>(
                                    mapOf(CreateRandomMinMaxXYClickView::actionList to actionList))
                        }
                        ActionType.RANDOM_MIN_MAX_WAIT -> {
                            this += find<CreateRandomMinMaxWaitView>(
                                    mapOf(CreateRandomMinMaxWaitView::actionList to actionList))
                        }
                    }
                } else {
                    println("ERROR - checkbox selection was null!")
                }
            }
        }
        println("left = $left")
        println("parent = $parent")
    }
}

class MouseKeyCaptureTestView : View("Mouse and Key Capture Test") {
    var clickCounter = 0
    var listening = true
    var click1x = -1
    var click1y = -1
    var click2x = -2
    var click2y = -2
    lateinit var theButton: Button

    val keyEventHandler = EventHandler<KeyEvent>() {
        when (clickCounter) {
            0 -> {
                println("clicked once:  ${it.character}")
                click1x = MouseInfo.getPointerInfo().location.x
                click1y = MouseInfo.getPointerInfo().location.y
            }
            1 -> {
                println("clicked twice: ${it.character}")
                click2x = MouseInfo.getPointerInfo().location.x
                click2y = MouseInfo.getPointerInfo().location.y
                listening = false
                theButton.fire()
            }
            else -> println("Oh dear, it didn't get removed")
        }
        clickCounter++
    }

    override val root = vbox {
        theButton = button("Capture 2 Clicks") {
            action {
                if (listening) {
                    clickCounter = 0
                    primaryStage.addEventHandler(KeyEvent.KEY_TYPED, keyEventHandler)
                } else {
                    primaryStage.removeEventHandler(KeyEvent.KEY_TYPED, keyEventHandler)
                    listening = true
                    println("First click ($click1x, $click1y)")
                    println("Second click ($click2x, $click2y)")
                }
            }
        }
    }
}

class MainView : View() {
    override val root = borderpane {
        primaryStage.width = 600.0
        primaryStage.height = 800.0
        top = menubar {
            menu("File") {
                menuitem("New Process") {
                    //                        replaceWith<AutomatedProcessView>()
                    replaceWith(find<AutomatedProcessView>(mapOf(AutomatedProcessView::actionList to mutableListOf<Action>())))
                }
                menuitem("Test click listener") {
                    replaceWith<MouseKeyCaptureTestView>()
                }
                separator()
                menuitem("Quit") {
                    Platform.exit()
                }
            }
        }
    }
}

class AutoAssistantApp : App(MainView::class) {
    init {
//        Platform.setImplicitExit(false)
    }
}

fun main(args: Array<String>) {
    launch<AutoAssistantApp>(args)
}