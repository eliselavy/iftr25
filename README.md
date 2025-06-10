# Exploring Luxembourg's Carnival through Digital Press Archives

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/eliselavy/iftr25/main?filepath=article.ipynb)

## Abstract

This research proposes to examine carnival celebrations in Luxembourg's two main urban centers through the lens of digitized historical newspapers, using the Impresso (https://impresso-project.ch/) platform's corpus and API. Our study aims to understand how carnival practices were reported and evolved in Luxembourg City and Esch-sur-Alzette, with particular attention to the period spanning both World Wars. By analyzing newspaper coverage, we will investigate several aspects of carnival culture: the types of events that received press attention, their locations (both indoor and outdoor venues), and their social accessibility as reflected in mask and ticket prices. The study will also explore how newspapers depicted different social groups and reported on public behavior during festivities. Our methodology combines basic text analysis with geographical mapping to track mentions of venues, events, and prices. Special attention will be given to specific carnival formats like the "bal travesti" and their evolution over time. We will also examine how commercial aspects of carnival were presented through advertisement analysis. The research will be conducted using Jupyter notebooks, making our methodology transparent and allowing other researchers to verify and build upon our findings. Through this initial exploration of Luxembourg's carnival traditions, we hope to contribute to our understanding of this important cultural practice while testing the potential of digital newspaper archives for cultural historical research.

## Project Structure

- `article.ipynb`  
  Main Jupyter notebook for data exploration, cleaning, and analysis. All steps are documented and reproducible.

- `script/`  
  Python scripts for data extraction, event parsing, and utility functions.

- `event.csv`  
  Extracted and structured event data, ready for further analysis or visualization.

- `dataset/`  
  Dataset from Impresso app https://impresso-project.ch/

- `media/`  
  Visual assets and diagrams used in the notebook.

- `abstract submission/Abstract.md`  
  Project abstract and submission text.

## How to Use

1. Launch the notebook using [MyBinder](https://mybinder.org/v2/gh/elisabethguerard/iftr25/HEAD) or clone the repository and run locally.
2. Follow the steps in `article.ipynb` to reproduce the analysis or adapt for your own research.
3. Scripts in the `script/` folder can be reused for similar digital humanities projects.

## Requirements

- Python 3.12+
- Jupyter Notebook
- pandas, matplotlib, plotly, dotenv, and other dependencies listed in `requirements.txt`

## License

MIT License
