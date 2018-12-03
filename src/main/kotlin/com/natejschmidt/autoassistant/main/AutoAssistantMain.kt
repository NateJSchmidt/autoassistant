package com.natejschmidt.autoassistant.main

import com.natejschmidt.autoassistant.actions.ActionType
import javafx.application.Platform
import javafx.beans.property.SimpleStringProperty
import javafx.collections.FXCollections
import tornadofx.*

class CreateActionView: View("Create Action") {
    override val root = vbox {
        val mutableListOfActionTypes = mutableListOf<String>()
        ActionType.values().forEach { mutableListOfActionTypes.add(it.strVal) }

        val actionTypes = FXCollections.observableArrayList(mutableListOfActionTypes)
        val selectedActionType = SimpleStringProperty()
        selectedActionType.onChange {
            println("new item selected: $it")
        }

        combobox(selectedActionType, actionTypes)
    }
}

class MainView : View() {
    override val root = borderpane {
        top {
            menubar {
                menu ("File") {
                    menuitem("New Process") {
                        replaceWith<CreateActionView>()
                    }
                    separator()
                    menuitem("Quit") {
                        Platform.exit()
                    }
                }
            }
        }
    }
}

class AutoAssistantApp : App(MainView::class)

fun main(args: Array<String>) {
    launch<AutoAssistantApp>(args)
}