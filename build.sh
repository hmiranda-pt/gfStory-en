#!/usr/bin/env bash
set -e
h_open_f="\e[1;34m:: \e[1;97m"
h_open="\n\e[1;34m:: \e[1;97m"
h_close="\e[0m"

echo -e "${h_open_f}Pulling submodules...${h_close}"
git submodule foreach git pull origin main

echo -e "${h_open}Setting up Python environment...${h_close}"
cd unpack
pdm install
source .venv/bin/activate
pip install -r downloader/requirements.txt
export TQDM_DISABLE=1

echo -e "${h_open}Downloading resources...${h_close}"
mkdir -p downloader/resdata
cp gf-data-us/resdata_no_hash.json downloader/resdata/us_resdata.json
cd downloader
sed -i 's/"ch"/"us"/' config.json5
git apply -q ../downloader.patch || true
zip -j resdata.zip resdata/us_resdata.json
python downloader.py --downloadres 0 --abname

echo -e "${h_open}Unpacking images...${h_close}"
cd ..
# Restore the committed formatted/ hjson set in the submodule. A previous run
# (or the downloader) can regenerate these with an incomplete set, dropping the
# campaign-to-chapter mappings. The fixed-data overlay below re-applies the two
# corrected files on top, so the checkout must precede it.
git -C gf-data-us checkout -- formatted/ || true
cp -r fixed-data/* gf-data-us
python tests/test_backgrounds.py
python tests/test_characters.py

echo -e "${h_open}Unpacking and converting audio files...${h_close}"
python tests/test_audio.py
reset -I || true

echo -e "${h_open}Processing resources...${h_close}"
python -m gfunpack downloader/output -o .

echo -e "${h_open}Moving resources...${h_close}"
cp audio/audio.json images/backgrounds.json images/characters.json stories/stories.json stories/chapters.json ../src/assets
if [[ -d "../public/audio" ]]; then
  rm -rf ../public/audio
fi
mv audio ../public
if [[ -d "../public/images" ]]; then
  rm -rf ../public/images
fi
mv images ../public
if [[ -d "../public/stories" ]]; then
  rm -rf ../public/stories
fi
mv stories ../public/stories

echo -e "${h_open}Building site...${h_close}"
cd ..
pnpm install
pnpm build-index
pnpm build

echo -e "\n\e[1;42mBUILD COMPLETE!\e[0m"
echo -e "\e[1;97mYour site is available at \e[1;33m$PWD/dist/\e[0m"
