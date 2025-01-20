import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QRadioButton, QButtonGroup, QTextEdit, QFormLayout, QStatusBar, QGroupBox, QRadioButton, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt
import PyQt5.QtGui as QGui
import PyQt5.QtCore as QCore

class RenderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Automatisation de Rendus')
        self.setGeometry(200, 200, 600, 400)

        # Variables
        self.scene_path = ""
        self.start_frame = ""
        self.end_frame = ""
        self.output_dir = ""
        self.render_layer = ""
        self.resolution = ""
        self.render_type = "1"

        # Layout principal
        main_layout = QVBoxLayout()

        # Création de widgets
        self.create_form_layout(main_layout)

        # Log section
        self.create_log_section(main_layout)

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage('Prêt à lancer le rendu.')
        main_layout.addWidget(self.status_bar)

        # Bouton de lancement
        launch_button = QPushButton("Lancer le rendu")
        launch_button.clicked.connect(self.start_render)
        main_layout.addWidget(launch_button)

        self.setLayout(main_layout)

    def create_form_layout(self, layout):
        form_layout = QFormLayout()

        # Scene path
        self.scene_path_input = QLineEdit(self)
        browse_button = QPushButton("Parcourir", self)
        browse_button.clicked.connect(self.open_file_dialog)
        browse_layout = QHBoxLayout()
        browse_layout.addWidget(self.scene_path_input)
        browse_layout.addWidget(browse_button)
        form_layout.addRow('Chemin de la scène Maya (.mb ou .ma) :', browse_layout)

        # Start frame
        self.start_frame_input = QLineEdit(self)
        form_layout.addRow('Frame de début :', self.start_frame_input)

        # End frame
        self.end_frame_input = QLineEdit(self)
        form_layout.addRow('Frame de fin :', self.end_frame_input)

        # Output directory
        self.output_dir_input = QLineEdit(self)
        output_dir_button = QPushButton("Parcourir", self)
        output_dir_button.clicked.connect(self.open_folder_dialog)
        browse_output_layout = QHBoxLayout()
        browse_output_layout.addWidget(self.output_dir_input)
        browse_output_layout.addWidget(output_dir_button)
        form_layout.addRow('Répertoire de sortie :', browse_output_layout)

        # Render Layer
        self.render_layer_input = QLineEdit(self)
        form_layout.addRow('Nom du Render Layer :', self.render_layer_input)

        # Resolution
        self.resolution_input = QLineEdit(self)
        form_layout.addRow('Résolution en pourcentage :', self.resolution_input)

        # Render Type (Radio buttons)
        self.create_render_type_section(form_layout)

        layout.addLayout(form_layout)

    def create_render_type_section(self, layout):
        group_box = QGroupBox("Type de rendu")
        radio_layout = QVBoxLayout()

        self.full_render_radio = QRadioButton("Rendu complet")
        self.fml_render_radio = QRadioButton("Rendu FML")
        self.full_render_radio.setChecked(True)  # Définit "Rendu complet" comme sélectionné par défaut

        radio_layout.addWidget(self.full_render_radio)
        radio_layout.addWidget(self.fml_render_radio)

        self.render_type_group = QButtonGroup(self)
        self.render_type_group.addButton(self.full_render_radio)
        self.render_type_group.addButton(self.fml_render_radio)

        group_box.setLayout(radio_layout)
        layout.addWidget(group_box)

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
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())  # Scroll automatique vers le bas

    def start_render(self):
        # Mettre à jour le statut
        self.status_bar.showMessage('Rendu en cours...', 2000)

        # Récupérer les valeurs des champs d'entrée
        scene_path = self.scene_path_input.text()
        start_frame = int(self.start_frame_input.text())
        end_frame = int(self.end_frame_input.text())
        output_dir = self.output_dir_input.text()
        render_layer = self.render_layer_input.text() if self.render_layer_input.text() else None
        percent_res = int(self.resolution_input.text()) if self.resolution_input.text() else 100
        render_type = "1" if self.full_render_radio.isChecked() else "2"

        try:
            # Lancer le rendu
            if render_type == "1":
                self.render_scene_full(scene_path, start_frame, end_frame, output_dir, render_layer, percent_res)
            elif render_type == "2":
                self.render_scene_fml(scene_path, start_frame, end_frame, output_dir, render_layer, percent_res)

            # Mettre à jour l'état après le rendu
            self.status_bar.showMessage('Rendu terminé avec succès.', 2000)
            self.log_message("Rendu terminé avec succès.")
        except Exception as e:
            self.status_bar.showMessage(f"Erreur : {str(e)}", 2000)
            self.log_message(f"Erreur : {str(e)}")

    def render_scene_full(self, scene_path, start_frame, end_frame, output_dir, render_layer=None, percent_res=100):
        self.log_message(f"\n=== Lancement du rendu complet pour la scène : {scene_path} ===")
        cmd = f'render -r arnold -s {start_frame} -e {end_frame} -rd {output_dir} -fnc name_#.ext -percentRes {percent_res} "{scene_path}"'
        if render_layer:
            cmd += f' -rl "{render_layer}"'
        self.log_message(f"Commande de rendu : {cmd}")
        subprocess.run(cmd, shell=True)
        self.log_message("\n=== Rendu complet terminé. ===")

    def render_scene_fml(self, scene_path, start_frame, end_frame, output_dir, render_layer=None, percent_res=100):
        self.log_message(f"\n=== Lancement du rendu FML pour la scène : {scene_path} ===")
        fml_frames = [start_frame]
        total_frames = end_frame - start_frame + 1
        mid_frame = start_frame + (total_frames // 2) - 1 if total_frames % 2 == 0 else start_frame + (total_frames // 2)
        fml_frames.append(mid_frame)
        fml_frames.append(end_frame)

        frames_str = ",".join(map(str, fml_frames))
        cmd = f'render -r arnold -s {start_frame} -e {end_frame} -percentRes {percent_res} -frames {frames_str} -rd "{output_dir}" -fnc name_#.ext "{scene_path}"'
        if render_layer:
            cmd += f' -rl "{render_layer}"'
        self.log_message(f"Commande de rendu : {cmd}")
        subprocess.run(cmd, shell=True)
        self.log_message("\n=== Rendu FML terminé. ===")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenderApp()
    window.show()
    sys.exit(app.exec_())
