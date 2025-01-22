import sys
import os
import subprocess
import configparser
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFileDialog, QRadioButton, QButtonGroup, QTextEdit, QFormLayout, QStatusBar, QGroupBox,
                             QDialog, QListWidget, QMessageBox)

class SettingsDialog(QDialog):
    def __init__(self, config_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres")
        self.setGeometry(300, 300, 500, 200)

        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

        maya_path = self.config.get("Paths", "MAYA_PATH", fallback="C:\\Program Files\\Autodesk\\Maya2024\\bin")
        qt_plugin_path = self.config.get("Paths", "QT_PLUGIN_PATH", fallback="C:\\Program Files\\Autodesk\\Maya2024\\plugins")

        layout = QFormLayout()

        self.maya_path_input = QLineEdit(maya_path)
        browse_maya_button = QPushButton("Parcourir")
        browse_maya_button.clicked.connect(self.browse_maya_path)
        maya_layout = QHBoxLayout()
        maya_layout.addWidget(self.maya_path_input)
        maya_layout.addWidget(browse_maya_button)
        layout.addRow("Chemin Maya (bin) :", maya_layout)

        self.qt_plugin_path_input = QLineEdit(qt_plugin_path)
        browse_qt_button = QPushButton("Parcourir")
        browse_qt_button.clicked.connect(self.browse_qt_plugin_path)
        qt_layout = QHBoxLayout()
        qt_layout.addWidget(self.qt_plugin_path_input)
        qt_layout.addWidget(browse_qt_button)
        layout.addRow("Chemin Qt Plugins :", qt_layout)

        save_button = QPushButton("Sauvegarder")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Annuler")
        cancel_button.clicked.connect(self.reject)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        layout.addRow(buttons_layout)

        self.setLayout(layout)

    def browse_maya_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner le chemin Maya (bin)")
        if folder:
            self.maya_path_input.setText(folder)

    def browse_qt_plugin_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner le chemin des plugins Qt")
        if folder:
            self.qt_plugin_path_input.setText(folder)

    def save_settings(self):
        if not self.config.has_section("Paths"):
            self.config.add_section("Paths")
        self.config.set("Paths", "MAYA_PATH", self.maya_path_input.text())
        self.config.set("Paths", "QT_PLUGIN_PATH", self.qt_plugin_path_input.text())

        with open(self.config_path, "w") as config_file:
            self.config.write(config_file)

        self.accept()

class RenderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.config_path = "config.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

        self.load_environment_paths()

        self.setWindowTitle('Automatisation de Rendus')
        self.setGeometry(200, 200, 600, 600)

        self.scene_path = ""
        self.start_frame = ""
        self.end_frame = ""
        self.output_dir = ""
        self.render_layer = ""
        self.resolution = ""

        self.render_queue = []  # Liste des rendus ajoutés

        main_layout = QVBoxLayout()

        self.create_form_layout(main_layout)
        self.create_render_queue_section(main_layout)
        self.create_log_section(main_layout)

        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage('Prêt à lancer le rendu.')
        main_layout.addWidget(self.status_bar)

        launch_button = QPushButton("Lancer")
        launch_button.clicked.connect(self.start_render)
        main_layout.addWidget(launch_button)

        settings_button = QPushButton("Paramètres")
        settings_button.clicked.connect(self.open_settings_dialog)
        main_layout.addWidget(settings_button)

        self.setLayout(main_layout)

    def load_environment_paths(self):
        maya_path = self.config.get("Paths", "MAYA_PATH", fallback="C:\\Program Files\\Autodesk\\Maya2024\\bin")
        qt_plugin_path = self.config.get("Paths", "QT_PLUGIN_PATH", fallback="C:\\Program Files\\Autodesk\\Maya2024\\plugins")

        os.environ["PATH"] = maya_path + ";" + os.environ["PATH"]
        os.environ["QT_PLUGIN_PATH"] = qt_plugin_path

    def create_form_layout(self, layout):
        form_layout = QFormLayout()

        self.scene_path_input = QLineEdit(self)
        browse_button = QPushButton("Parcourir", self)
        browse_button.clicked.connect(self.open_file_dialog)
        browse_layout = QHBoxLayout()
        browse_layout.addWidget(self.scene_path_input)
        browse_layout.addWidget(browse_button)
        form_layout.addRow('Chemin de la scène Maya (.mb ou .ma) :', browse_layout)

        self.start_frame_input = QLineEdit(self)
        form_layout.addRow('Frame de début :', self.start_frame_input)

        self.end_frame_input = QLineEdit(self)
        form_layout.addRow('Frame de fin :', self.end_frame_input)

        self.output_dir_input = QLineEdit(self)
        output_dir_button = QPushButton("Parcourir", self)
        output_dir_button.clicked.connect(self.open_folder_dialog)
        browse_output_layout = QHBoxLayout()
        browse_output_layout.addWidget(self.output_dir_input)
        browse_output_layout.addWidget(output_dir_button)
        form_layout.addRow('Répertoire de sortie :', browse_output_layout)

        self.render_layer_input = QLineEdit(self)
        form_layout.addRow('Nom du Render Layer :', self.render_layer_input)

        self.resolution_input = QLineEdit(self)
        form_layout.addRow('Résolution en pourcentage :', self.resolution_input)

        render_type_group = QGroupBox("Type de rendu")
        render_type_layout = QHBoxLayout()

        self.full_render_radio = QRadioButton("Rendu complet", self)
        self.fml_render_radio = QRadioButton("Rendu rapide (FML)", self)
        self.full_render_radio.setChecked(True)

        render_type_layout.addWidget(self.full_render_radio)
        render_type_layout.addWidget(self.fml_render_radio)
        render_type_group.setLayout(render_type_layout)
        form_layout.addRow(render_type_group)

        add_render_button = QPushButton("Ajouter à la file d'attente")
        add_render_button.clicked.connect(self.add_render_to_queue)
        form_layout.addRow(add_render_button)

        layout.addLayout(form_layout)

    def create_render_queue_section(self, layout):
        self.render_queue_list = QListWidget(self)
        layout.addWidget(QLabel("File d'attente des rendus :"))
        layout.addWidget(self.render_queue_list)

        remove_button = QPushButton("Supprimer le rendu sélectionné")
        remove_button.clicked.connect(self.remove_selected_render)
        layout.addWidget(remove_button)

    def create_log_section(self, layout):
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Ouvrir la scène Maya", "", "Fichiers Maya (*.mb *.ma)")
        if filename:
            self.scene_path_input.setText(filename)

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner le répertoire de sortie")
        if folder:
            self.output_dir_input.setText(folder)

    def log_message(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def add_render_to_queue(self):
        scene_path = self.scene_path_input.text()
        start_frame = self.start_frame_input.text()
        end_frame = self.end_frame_input.text()
        output_dir = self.output_dir_input.text()
        render_layer = self.render_layer_input.text()
        resolution = self.resolution_input.text()

        if not scene_path or not start_frame or not end_frame or not output_dir:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        render_details = {
            "scene_path": scene_path,
            "start_frame": start_frame,
            "end_frame": end_frame,
            "output_dir": output_dir,
            "render_layer": render_layer,
            "resolution": resolution,
            "type": "full" if self.full_render_radio.isChecked() else "fml"
        }

        self.render_queue.append(render_details)
        self.render_queue_list.addItem(f"Scène : {scene_path}, Frames : {start_frame}-{end_frame}, Type : {'Full' if self.full_render_radio.isChecked() else 'FML'}")
        self.log_message("Rendu ajouté à la file d'attente.")

    def remove_selected_render(self):
        selected_row = self.render_queue_list.currentRow()
        if selected_row >= 0:
            self.render_queue.pop(selected_row)
            self.render_queue_list.takeItem(selected_row)
            self.log_message("Rendu supprimé de la file d'attente.")

    def start_render(self):
        if self.render_queue:
            self.start_render_queue()
        else:
            self.start_single_render()

    def start_single_render(self):
        scene_path = self.scene_path_input.text()
        start_frame = self.start_frame_input.text()
        end_frame = self.end_frame_input.text()
        output_dir = self.output_dir_input.text()
        render_layer = self.render_layer_input.text()
        resolution = self.resolution_input.text()

        if not scene_path or not start_frame or not end_frame or not output_dir:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        try:
            if self.full_render_radio.isChecked():
                self.render_scene_full(scene_path, int(start_frame), int(end_frame), output_dir, render_layer, int(resolution or 100))
            else:
                self.render_scene_fml(scene_path, int(start_frame), int(end_frame), output_dir, render_layer, int(resolution or 100))

            self.log_message("Rendu unique terminé.")
        except Exception as e:
            self.log_message(f"Erreur lors du rendu unique : {str(e)}")

    def start_render_queue(self):
        for render in self.render_queue:
            if render["type"] == "full":
                self.render_scene_full(
                    render["scene_path"],
                    int(render["start_frame"]),
                    int(render["end_frame"]),
                    render["output_dir"],
                    render["render_layer"],
                    int(render["resolution"] or 100)
                )
            else:
                self.render_scene_fml(
                    render["scene_path"],
                    int(render["start_frame"]),
                    int(render["end_frame"]),
                    render["output_dir"],
                    render["render_layer"],
                    int(render["resolution"] or 100)
                )

        self.log_message("Tous les rendus dans la file d'attente ont été exécutés.")
        self.render_queue.clear()
        self.render_queue_list.clear()

    def render_scene_full(self, scene_path, start_frame, end_frame, output_dir, render_layer=None, percent_res=100):
        self.log_message(f"\n=== Lancement du rendu complet pour la scène : {scene_path} ===")
        cmd = f'render -r arnold -s {start_frame} -e {end_frame} -rd {output_dir} -fnc name_#.ext -percentRes {percent_res}'
        if render_layer:
            cmd += f' -rl {render_layer}'
        cmd += f' "{scene_path}"'
        self.log_message(f"Commande de rendu : {cmd}")
        subprocess.run(cmd, shell=True)
        self.log_message("\n=== Rendu complet terminé. ===")

    def render_scene_fml(self, scene_path, start_frame, end_frame, output_dir, render_layer=None, percent_res=100):
        self.log_message(f"\n=== Lancement du rendu rapide (FML) pour la scène : {scene_path} ===")
        total_frames = end_frame - start_frame + 1
        mid_frame = start_frame + (total_frames // 2)

        frames = [start_frame, mid_frame, end_frame]

        for frame in frames:
            cmd = f'render -r arnold -s {frame} -e {frame} -rd {output_dir} -fnc name_#.ext -percentRes {percent_res}'
            if render_layer:
                cmd += f' -rl {render_layer}'
            cmd += f' "{scene_path}"'
            self.log_message(f"Commande de rendu pour frame {frame} : {cmd}")
            subprocess.run(cmd, shell=True)

        self.log_message("\n=== Rendu rapide (FML) terminé. ===")

    def open_settings_dialog(self):
        dialog = SettingsDialog(self.config_path, self)
        if dialog.exec_():
            self.load_environment_paths()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenderApp()
    window.show()
    sys.exit(app.exec_())