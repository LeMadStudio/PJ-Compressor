import sys
import subprocess
import importlib.util
import os

def check_and_install_libraries():
    """
    Vérifie si les bibliothèques requises sont installées et les installe si nécessaire
    """
    print("Vérification des dépendances nécessaires...")
    
    # Liste des bibliothèques requises
    required_libraries = {
        "PIL": "pillow",       # Pour le traitement des images
        "PyPDF2": "PyPDF2",    # Pour la manipulation basique des PDF
    }
    
    # Vérification et installation des bibliothèques
    for lib_name, pip_name in required_libraries.items():
        if not is_library_installed(lib_name):
            print(f"{lib_name} n'est pas installé. Installation en cours...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
                print(f"{lib_name} a été installé avec succès.")
            except subprocess.CalledProcessError:
                print(f"Erreur lors de l'installation de {lib_name}. Veuillez l'installer manuellement avec : pip install {pip_name}")
                return False
        else:
            print(f"{lib_name} est déjà installé.")
    
    # Vérifier si Ghostscript est installé
    if not is_ghostscript_installed():
        print("\nGhostscript n'est pas installé ou n'est pas dans le PATH.")
        print("La compression PDF sera limitée sans Ghostscript.")
        print("\nInstructions d'installation de Ghostscript :")
        print("- Windows : Télécharger et installer depuis https://www.ghostscript.com/download.html")
        print("- macOS : brew install ghostscript")
        print("- Linux : sudo apt-get install ghostscript")
        print("\nL'application fonctionnera sans Ghostscript, mais la compression PDF sera moins efficace.")
    else:
        print("Ghostscript est installé et disponible.")
    
    print("\nToutes les dépendances Python ont été vérifiées.")
    return True

def is_library_installed(library_name):
    """
    Vérifie si une bibliothèque Python est installée
    """
    return importlib.util.find_spec(library_name) is not None

def is_ghostscript_installed():
    """
    Vérifie si Ghostscript est installé
    """
    try:
        # Tente d'exécuter la commande gs --version
        subprocess.run(
            ["gs", "--version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

# Exécuter la vérification des bibliothèques avant d'importer les modules
if __name__ == "__main__":
    # Vérifier et installer les bibliothèques
    if check_and_install_libraries():
        print("Démarrage de l'application...")
        
        # Maintenant qu'on est sûr que les bibliothèques sont installées, on peut les importer
        import tkinter as tk
        from tkinter import filedialog, ttk, messagebox
        from PIL import Image, ImageFile
        import threading
        import shutil
        import tempfile
        from PyPDF2 import PdfReader, PdfWriter
        
        # Permet à Pillow de traiter des images potentiellement corrompues
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        
        class CompressionApp:
            def __init__(self, root):
                self.root = root
                self.root.title("Compression des PJ Comptables")
                self.root.geometry("700x500")
                self.root.resizable(True, True)
                
                # Variables
                self.source_folder = tk.StringVar()
                self.destination_folder = tk.StringVar()
                self.compression_level = tk.StringVar(value="moyenne")
                self.create_copies = tk.BooleanVar(value=True)
                self.compression_running = False
                
                # Configuration du style
                self.style = ttk.Style()
                self.style.configure("TButton", font=("Arial", 10))
                self.style.configure("TLabel", font=("Arial", 10))
                self.style.configure("Header.TLabel", font=("Arial", 12, "bold"))
                
                # Création de l'interface
                self.create_widgets()
                
                # Définir les niveaux de compression (qualité/dpi)
                self.compression_settings = {
                    "légère": {"image_quality": 90, "pdf_dpi": 150},
                    "moyenne": {"image_quality": 75, "pdf_dpi": 120},
                    "forte": {"image_quality": 50, "pdf_dpi": 90}
                }
            
            def create_widgets(self):
                # Frame principale
                main_frame = ttk.Frame(self.root, padding=20)
                main_frame.pack(fill=tk.BOTH, expand=True)
                
                # Titre
                title_label = ttk.Label(
                    main_frame, 
                    text="Compression des pièces jointes comptables", 
                    style="Header.TLabel"
                )
                title_label.pack(pady=(0, 20))
                
                # Section Dossier Source
                source_frame = ttk.LabelFrame(main_frame, text="Dossier Source", padding=10)
                source_frame.pack(fill=tk.X, pady=5)
                
                source_entry = ttk.Entry(source_frame, textvariable=self.source_folder, width=50)
                source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
                
                source_button = ttk.Button(
                    source_frame, 
                    text="Parcourir...", 
                    command=self.browse_source
                )
                source_button.pack(side=tk.RIGHT)
                
                # Section Dossier Destination
                dest_frame = ttk.LabelFrame(main_frame, text="Dossier Destination", padding=10)
                dest_frame.pack(fill=tk.X, pady=5)
                
                dest_entry = ttk.Entry(dest_frame, textvariable=self.destination_folder, width=50)
                dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
                
                dest_button = ttk.Button(
                    dest_frame, 
                    text="Parcourir...", 
                    command=self.browse_destination
                )
                dest_button.pack(side=tk.RIGHT)
                
                # Section Options
                options_frame = ttk.LabelFrame(main_frame, text="Options", padding=10)
                options_frame.pack(fill=tk.X, pady=5)
                
                # Option Niveau de compression
                compression_label = ttk.Label(options_frame, text="Niveau de compression:")
                compression_label.grid(row=0, column=0, sticky=tk.W, pady=5)
                
                compression_frame = ttk.Frame(options_frame)
                compression_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
                
                # Boutons radio pour les niveaux de compression
                ttk.Radiobutton(
                    compression_frame, 
                    text="Légère", 
                    variable=self.compression_level, 
                    value="légère"
                ).pack(side=tk.LEFT, padx=(0, 10))
                
                ttk.Radiobutton(
                    compression_frame, 
                    text="Moyenne", 
                    variable=self.compression_level, 
                    value="moyenne"
                ).pack(side=tk.LEFT, padx=(0, 10))
                
                ttk.Radiobutton(
                    compression_frame, 
                    text="Forte", 
                    variable=self.compression_level, 
                    value="forte"
                ).pack(side=tk.LEFT)
                
                # Option Copie
                copy_check = ttk.Checkbutton(
                    options_frame, 
                    text="Créer des copies (ne pas écraser les originaux)", 
                    variable=self.create_copies
                )
                copy_check.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
                
                # Section Logs
                log_frame = ttk.LabelFrame(main_frame, text="Journal", padding=10)
                log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
                
                # Scrollbar pour les logs
                scrollbar = ttk.Scrollbar(log_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                self.log_text = tk.Text(log_frame, height=10, width=50, yscrollcommand=scrollbar.set)
                self.log_text.pack(fill=tk.BOTH, expand=True)
                scrollbar.config(command=self.log_text.yview)
                
                # Barre de progression
                self.progress_var = tk.DoubleVar()
                self.progress_bar = ttk.Progressbar(
                    main_frame, 
                    orient=tk.HORIZONTAL, 
                    length=100, 
                    mode='determinate', 
                    variable=self.progress_var
                )
                self.progress_bar.pack(fill=tk.X, pady=(10, 5))
                
                # Boutons
                buttons_frame = ttk.Frame(main_frame)
                buttons_frame.pack(fill=tk.X, pady=5)
                
                self.compress_button = ttk.Button(
                    buttons_frame, 
                    text="Démarrer la compression", 
                    command=self.start_compression,
                    width=25
                )
                self.compress_button.pack(side=tk.RIGHT, padx=5)
                
                cancel_button = ttk.Button(
                    buttons_frame, 
                    text="Quitter", 
                    command=self.root.destroy,
                    width=15
                )
                cancel_button.pack(side=tk.RIGHT, padx=5)
            
            def browse_source(self):
                folder = filedialog.askdirectory(title="Sélectionner le dossier source")
                if folder:
                    self.source_folder.set(folder)
                    self.log("Dossier source sélectionné: " + folder)
            
            def browse_destination(self):
                folder = filedialog.askdirectory(title="Sélectionner le dossier destination")
                if folder:
                    self.destination_folder.set(folder)
                    self.log("Dossier destination sélectionné: " + folder)
            
            def log(self, message):
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
                # Pour s'assurer que les messages sont visibles immédiatement
                self.root.update_idletasks()
            
            def start_compression(self):
                if self.compression_running:
                    messagebox.showwarning("En cours", "Compression déjà en cours!")
                    return
                
                source = self.source_folder.get()
                destination = self.destination_folder.get()
                
                if not source or not os.path.isdir(source):
                    messagebox.showerror("Erreur", "Veuillez sélectionner un dossier source valide!")
                    return
                
                if not destination and self.create_copies.get():
                    messagebox.showerror("Erreur", "Veuillez sélectionner un dossier destination!")
                    return
                
                if not self.create_copies.get():
                    confirm = messagebox.askyesno(
                        "Confirmation",
                        "Les fichiers originaux seront écrasés. Continuer?"
                    )
                    if not confirm:
                        return
                
                # Vérifier si Ghostscript est installé pour la compression PDF
                gs_installed = is_ghostscript_installed()
                if not gs_installed:
                    self.log("Avertissement: Ghostscript n'est pas installé ou disponible dans le PATH.")
                    self.log("La compression PDF sera limitée. Considérez installer Ghostscript pour de meilleurs résultats.")
                
                # Démarrer la compression dans un thread séparé
                self.compression_running = True
                self.compress_button.config(state=tk.DISABLED)
                threading.Thread(target=self.compress_files, daemon=True).start()
            
            def compress_files(self):
                try:
                    source = self.source_folder.get()
                    destination = self.destination_folder.get()
                    comp_level = self.compression_level.get()
                    create_copies = self.create_copies.get()
                    
                    # Récupérer les paramètres de compression
                    image_quality = self.compression_settings[comp_level]["image_quality"]
                    pdf_dpi = self.compression_settings[comp_level]["pdf_dpi"]
                    
                    self.log(f"Niveau de compression sélectionné: {comp_level}")
                    self.log(f"Qualité d'image: {image_quality}, DPI pour PDF: {pdf_dpi}")
                    
                    # Lister tous les fichiers à traiter
                    all_files = []
                    for root, _, files in os.walk(source):
                        for file_name in files:
                            if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                                file_path = os.path.join(root, file_name)
                                all_files.append(file_path)
                    
                    if not all_files:
                        self.log("Aucun fichier à compresser trouvé dans le dossier source.")
                        self.finish_compression()
                        return
                    
                    self.log(f"Nombre de fichiers à traiter: {len(all_files)}")
                    
                    # Initialiser la barre de progression
                    self.progress_var.set(0)
                    processed = 0
                    saved_space = 0
                    
                    for file_path in all_files:
                        # Récupérer la taille initiale
                        initial_size = os.path.getsize(file_path)
                        
                        # Déterminer le chemin de destination
                        rel_path = os.path.relpath(file_path, source)
                        dest_path = os.path.join(destination, rel_path) if create_copies else file_path
                        
                        if create_copies:
                            # Créer les dossiers de destination si nécessaire
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                            # Copier le fichier
                            shutil.copy2(file_path, dest_path)
                            file_to_compress = dest_path
                        else:
                            file_to_compress = file_path
                        
                        # Compression selon le type de fichier
                        file_ext = os.path.splitext(file_path)[1].lower()
                        if file_ext in ['.png', '.jpg', '.jpeg']:
                            success = self.compress_image(file_to_compress, image_quality)
                        elif file_ext == '.pdf':
                            success = self.compress_pdf(file_to_compress, pdf_dpi)
                        else:
                            success = False
                        
                        # Calculer l'espace gagné si la compression a réussi
                        if success:
                            final_size = os.path.getsize(file_to_compress)
                            file_saved = initial_size - final_size
                            saved_space += file_saved
                            
                            # Informations sur la taille (en KB pour plus de lisibilité)
                            if file_saved > 0:
                                self.log(f"{os.path.basename(file_path)}: {initial_size/1024:.1f} KB → {final_size/1024:.1f} KB (-{file_saved/1024:.1f} KB)")
                            else:
                                self.log(f"{os.path.basename(file_path)}: Pas de réduction de taille significative")
                        
                        # Mettre à jour la progression
                        processed += 1
                        progress = (processed / len(all_files)) * 100
                        self.progress_var.set(progress)
                        
                        # Mettre à jour l'interface
                        if processed % 5 == 0 or processed == len(all_files):
                            self.root.update_idletasks()
                    
                    # Rapport final
                    if saved_space > 0:
                        if saved_space > 1024*1024:
                            self.log(f"Compression terminée! Espace total économisé: {saved_space/(1024*1024):.2f} MB")
                        else:
                            self.log(f"Compression terminée! Espace total économisé: {saved_space/1024:.2f} KB")
                    else:
                        self.log("Compression terminée! Aucune réduction significative de taille n'a été obtenue.")
                    
                    messagebox.showinfo("Terminé", "Compression des fichiers terminée avec succès!")
                    
                except Exception as e:
                    self.log(f"Erreur lors de la compression: {str(e)}")
                    messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
                
                finally:
                    self.finish_compression()
            
            def finish_compression(self):
                self.compression_running = False
                self.compress_button.config(state=tk.NORMAL)
            
            def compress_image(self, file_path, quality=75):
                """Compresse une image avec la qualité spécifiée"""
                try:
                    with Image.open(file_path) as img:
                        # Vérifier le mode de l'image (convertir si nécessaire)
                        if img.mode in ("RGBA", "P"):
                            # Convertir les images avec transparence en RGB
                            img = img.convert("RGB")
                        
                        # Sauvegarder l'image compressée
                        img.save(file_path, optimize=True, quality=quality)
                        return True
                        
                except Exception as e:
                    self.log(f"Erreur lors de la compression de {os.path.basename(file_path)}: {str(e)}")
                    return False
            
            def compress_pdf(self, file_path, dpi=120):
                """Compresse un PDF en utilisant Ghostscript si disponible, sinon utilise une méthode alternative"""
                try:
                    # Vérifier si Ghostscript est installé
                    if is_ghostscript_installed():
                        # Méthode avec Ghostscript (plus efficace)
                        return self.compress_pdf_ghostscript(file_path, dpi)
                    else:
                        # Méthode alternative (moins efficace mais sans dépendance externe)
                        return self.compress_pdf_alternative(file_path)
                        
                except Exception as e:
                    self.log(f"Erreur lors de la compression de {os.path.basename(file_path)}: {str(e)}")
                    return False
            
            def compress_pdf_ghostscript(self, file_path, dpi=120):
                """Compresse un PDF en utilisant Ghostscript (méthode plus efficace)"""
                try:
                    # Création d'un fichier temporaire
                    fd, temp_file = tempfile.mkstemp(suffix='.pdf')
                    os.close(fd)
                    
                    # Déterminer le niveau de compression basé sur le DPI
                    if dpi >= 150:
                        preset = '/printer'  # Légère compression
                    elif dpi >= 100:
                        preset = '/ebook'    # Compression moyenne
                    else:
                        preset = '/screen'   # Forte compression
                    
                    # Construire la commande Ghostscript
                    gs_command = [
                        'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                        f'-dPDFSETTINGS={preset}', '-dNOPAUSE', '-dQUIET', '-dBATCH',
                        f'-sOutputFile={temp_file}', file_path
                    ]
                    
                    # Exécuter Ghostscript
                    result = subprocess.run(gs_command, check=True, capture_output=True)
                    
                    # Vérifier si le fichier temporaire existe et a une taille
                    if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                        # Remplacer l'original par le compressé
                        os.replace(temp_file, file_path)
                        return True
                    else:
                        self.log(f"Erreur: Ghostscript n'a pas créé de fichier valide pour {os.path.basename(file_path)}")
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                        return False
                        
                except subprocess.SubprocessError as e:
                    self.log(f"Erreur Ghostscript: {str(e)}")
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    return False
                    
                except Exception as e:
                    self.log(f"Erreur lors de la compression PDF: {str(e)}")
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    return False
            
            def compress_pdf_alternative(self, file_path):
                """
                Méthode alternative pour la compression PDF quand Ghostscript n'est pas disponible.
                Cette méthode est moins efficace mais fonctionne sans dépendance externe.
                """
                try:
                    # Création d'un nom temporaire pour le fichier compressé
                    temp_file = file_path + ".temp"
                    
                    # Lecture du PDF original
                    reader = PdfReader(file_path)
                    writer = PdfWriter()
            
                    # Copie de chaque page avec compression
                    for page in reader.pages:
                        # Ajouter la page au nouveau document
                        writer.add_page(page)
                    
                    # Préserver les métadonnées
                    if hasattr(reader, 'metadata') and reader.metadata:
                        writer.add_metadata(reader.metadata)
                    
                    # Compresser les streams disponibles avec PyPDF2
                    for page in writer._objects:
                        if hasattr(page, '/Contents') and page['/Contents']:
                            writer._objects[page['/Contents']].compress()
                    
                    # Écriture du fichier compressé
                    with open(temp_file, "wb") as f:
                        writer.write(f)
                    
                    # Vérifier si le fichier temporaire existe et a une taille
                    if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                        # Remplacer l'original par le compressé
                        os.replace(temp_file, file_path)
                        return True
                    else:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                        return False
                        
                except Exception as e:
                    self.log(f"Erreur méthode alternative PDF: {str(e)}")
                    if 'temp_file' in locals() and os.path.exists(temp_file):
                        os.remove(temp_file)
                    return False

        # Lancer l'application
        root = tk.Tk()
        app = CompressionApp(root)
        root.mainloop()
    else:
        print("Impossible de démarrer l'application en raison de dépendances manquantes.")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)