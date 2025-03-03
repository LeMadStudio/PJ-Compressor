# PJ-Compressor
Outil Python de compression de pièces jointes (JPG, PNG, PDF)
# Compresseur de Pièces Jointes Comptables

Outil Python avec une interface graphique vous permettant de compresser facilement des fichiers PDF et images utilisés comme pièces jointes dans par exemple lors d'imports sur des logiciels de comptabilité.

![image](https://github.com/user-attachments/assets/8e867f67-1397-478a-9ccd-4b338e39ad3d)

## 📋 Fonctionnalités

- **Compression intelligente** des fichiers PDF et images (PNG, JPG, JPEG)
- **Interface graphique intuitive** pour une utilisation sans connaissances techniques
- **3 niveaux de compression** : légère, moyenne et forte
- **Mode copie** : crée des versions compressées sans modifier les originaux
- **Journal détaillé** montrant les taux de compression et économies d'espace
- **Préservation de la structure** des dossiers lors de la compression
- **Installation automatique** des dépendances requises

## 🔧 Prérequis

- **Python 3.6+** installé sur votre système
- Les dépendances seront automatiquement installées au premier lancement :
  - Pillow (traitement d'images)
  - PyPDF2 (manipulation basique des PDF)

### Recommandé pour une compression PDF optimale :

- **Ghostscript** : permet une compression PDF beaucoup plus efficace
  - Windows : [Télécharger Ghostscript](https://www.ghostscript.com/download/gsdnld.html)
  - macOS : `brew install ghostscript`
  - Linux : `sudo apt install ghostscript` ou équivalent

## 💻 Installation

### Téléchargement

```bash
# Cloner le dépôt
git clone https://github.com/votre-nom/compresseur-pj.git
cd compresseur-pj

# Ou télécharger le fichier ZIP depuis GitHub et l'extraire
```

### Lancement

```bash
# Lancer l'application
python compresseur_pj.py
```

L'application vérifiera et installera automatiquement les dépendances Python nécessaires lors du premier lancement.

## 📝 Guide d'utilisation

1. **Démarrage de l'application**
   - Lancez `compresseur_pj.py` avec Python
   - L'application vérifiera automatiquement les dépendances requises

2. **Sélection des dossiers**
   - Cliquez sur "Parcourir..." pour sélectionner le dossier source contenant vos fichiers
   - Sélectionnez un dossier destination si vous souhaitez créer des copies compressées

3. **Configuration**
   - Choisissez le niveau de compression :
     - **Légère** : qualité d'image 90% / PDF 150 DPI (réduction de taille minimale)
     - **Moyenne** : qualité d'image 75% / PDF 120 DPI (recommandé)
     - **Forte** : qualité d'image 50% / PDF 90 DPI (réduction maximale)
   - Cochez "Créer des copies" pour préserver les originaux, ou décochez pour les remplacer

4. **Compression**
   - Cliquez sur "Démarrer la compression"
   - Suivez la progression dans la barre d'état et le journal
   - Une notification apparaîtra lorsque la compression sera terminée

5. **Résultats**
   - Le journal affiche les détails de chaque fichier compressé
   - L'économie d'espace totale est calculée et affichée à la fin

## ⚙️ Niveaux de compression

| Niveau  | Images (qualité) | PDF (préréglage) | Utilisation recommandée |
|---------|------------------|------------------|-------------------------|
| Légère  | 90%              | /printer (150 DPI) | Documents officiels, qualité primordiale |
| Moyenne | 75%              | /ebook (120 DPI)   | Équilibre qualité/taille (recommandé) |
| Forte   | 50%              | /screen (90 DPI)   | Archivage, optimisation maximale d'espace |

## 🔍 Résolution de problèmes

### Compression PDF inefficace

Si la compression PDF ne réduit pas suffisamment la taille :

1. Vérifiez que Ghostscript est correctement installé
2. Assurez-vous que la commande `gs` est accessible dans le chemin système
3. Essayez un niveau de compression plus élevé

### Erreurs lors de la compression d'images

Si certaines images ne peuvent pas être compressées :

1. Vérifiez que les fichiers ne sont pas corrompus
2. Assurez-vous qu'ils ne sont pas ouverts dans un autre programme
3. Consultez le journal pour des messages d'erreur spécifiques

## 🛠️ Développement et personnalisation

Le code source est commenté et structuré pour faciliter la personnalisation :

- **Niveaux de compression** : modifiez les valeurs dans `compression_settings` pour ajuster les paramètres
- **Types de fichiers** : ajoutez d'autres extensions dans les conditions `file_name.lower().endswith()`
- **Interface** : personnalisez les éléments dans la méthode `create_widgets()`

## 📄 Licence

Ce projet est distribué sous licence MIT (open source). 


## 🙏 Remerciements

- Bibliothèque PIL/Pillow pour le traitement d'images
- PyPDF2 pour la manipulation basique des PDF
- Ghostscript pour la compression PDF avancée

---

Développé pour faciliter le travail des équipes comptables lors de l'import de pièces jointes dans les logiciels comptables.
