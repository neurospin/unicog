
import os

#path results
path_results_pypreprocess = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/fmri_results"

path_results_surface = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm"

#Lists
subjects = ['subject01','subject02','subject03','subject04',
            'subject05','subject06','subject07','subject08',
            'subject09','subject10','subject11','subject12',
            'subject13','subject14'][0:2]

#Contrast       
contrasts = [['h_checkerboard','damier_H'],
            ['v_checkerboard',  'damier_V'],
            ['r_hand_audio', 'clicDaudio'],
            ['l_hand_audio','clicGaudio'],
            ['r_hand_video',  'clicDvideo'],
            ['l_hand_video', 'clicGvideo'],
            ['computation_audio', 'calculaudio'],
            ['computation_video','calculvideo'],
            ['sentence_video', 'phrasevideo'],
            ['sentence_audio','phraseaudio'], 
            ['loc_audio', "audio"],
            ["loc_video", "video"],
            ["left"],
            ["right"], 
            ["computation"],
            ["sentences"],
            ["H-V"], 
            ["V-H"], 
            ["left-right"],
            ["right-left"], 
            ['motor-cognitive'],  
            ["audio-video"], 
            ["video-audio"], 
            ["computation-sentences"], 
            ["reading-visual"]][0:2]


content = ""
#file_img = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/snapshot/filter_H-V_z_maplh.png"
#image = "![]({file_img}\b=\b50x50)".format(file_img=file_img)
#image = "![]({file_img})".format(file_img=file_img)

#<img src="/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/snapshot/filter_H-V_z_maplh.png" width="200" height="150">

#Loop
for sbj in subjects:
    for con in contrasts:
        path = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/snapshot/filter_H-V_z_maplh.png"
        image = '<a href ="{image}" width="300" height="200"><img src="{image}" width="300" height="200"</a>'.format(image=path)
        line = "\nVolume-based GLM results for {sbj} and {con}\n\n".format(
                sbj=sbj, con=con)
        content += line 
        tab += "| {image}       \n".format(image=image)
        content += tab
        
        line = "\n\nSurface-based GLM results for {sbj} and {con}\n\n".format(
                sbj=sbj, con=con)
        content += line 
        tab =  "| header 1      | header 2      | header 3  |\n"
        tab += "| ------------- |:-------------:| ---------:|\n"
        tab += "| {image}       | {image}       |   {image} |\n".format(image=image)
        content += tab

path_summary = "/home/id983365/temp/file.md"
file_summary = open(path_summary, "w")
file_summary.write(content)
file_summary.close()

#convert in html
path_html = "/home/id983365/temp/file.html"
cmd = "pandoc -s -S --toc {md} -o {output}".format(md=path_summary, output=path_html)
os.system(cmd)