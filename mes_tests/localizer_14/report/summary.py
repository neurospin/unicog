
import os
import glob

#path data
path_data = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data"

#path summary
path_summary = os.path.join(path_data, "summary")
path_md =  os.path.join(path_summary, "tmp.md")
path_html = os.path.join(path_summary, "report_display.html")

#path results
path_results_pypreprocess = os.path.join(path_data, 'fmri_results')
path_results_surface = os.path.join(path_data, 'surface_glm')

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
            ["reading-visual"]][21:22]

def write_tag_image(con, subject, path):
    liste_images = []
    hemis = ['rh', 'lh']
    views = ['medial', 'lateral']
    for hemi in hemis:
        for view in views:
          image = ""  
          for c in con :
              path_file = glob.glob(path + '/' + subject + '/snapshots/' + c + '*' + hemi + '_' + view + '*')
              tmp = path + '/' + subject + '/snapshots/' + c + '*' + hemi + '_' + view + '*'         
              print tmp              
              print path_file
              if path_file :
                  print "yeah"
                  image = '<a href ="{image}" width="300" height="200"><img src="{image}" \
                    width="300" height="200"</a>'.format(image=path_file[0])
              liste_images.append(image)
    return liste_images

content = ""
#file_img = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/snapshot/filter_H-V_z_maplh.png"
#image = "![]({file_img}\b=\b50x50)".format(file_img=file_img)
#image = "![]({file_img})".format(file_img=file_img)

#<img src="/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/data/surface_glm/snapshot/filter_H-V_z_maplh.png" width="200" height="150">

#Loop
for sbj in subjects:
    
    for con in contrasts:
        #Volume glm
#        path = "/neurospin/unicog/protocols/IRMf/Tests_Isa/Test_surface_glm/ \
#                data/surface_glm/snapshot/filter_H-V_z_maplh.png"
#                
#        image = '<a href ="{image}" width="300" height="200"><img src="{image}" \
#                width="300" height="200"</a>'.format(image=path)
#        line = "\nVolume-based GLM results for {sbj} and {con}\n\n".format(
#                sbj=sbj, con=con)
#        content += line 
#        tab += "| {image}       \n".format(image=image)
#        content += tab
        
        #Surface glm
        paths_img_volume = write_tag_image(con, sbj, path_results_surface)
        paths_img_texture = write_tag_image(con, sbj, path_results_surface)
        paths_img_texture_filter = write_tag_image(con, sbj, path_results_surface)
        
        print paths_img_texture
#        image1 = '<a href ="{image}" width="300" height="200"><img src="{image}" \
#        width="300" height="200"</a>'.format(image=path)
#        image2 = '<a href ="{image}" width="300" height="200"><img src="{image}" \
#        width="300" height="200"</a>'.format(image=path)
#        
#        paths = write_tag_image(con, sbj, path_results_surface)
#        image3 = '<a href ="{image}" width="300" height="200"><img src="{image}" \
#        width="300" height="200"</a>'.format(image=path)
#        image4 = '<a href ="{image}" width="300" height="200"><img src="{image}" \
#        width="300" height="200"</a>'.format(image=path)
#        
#        paths = write_tag_image(con, sbj, path_results_surface)
#        image5 = '<a href ="{image}" width="300" height="200"><img src="{image}" \
#        width="300" height="200"</a>'.format(image=path)
#        image6 = '<a href ="{image}" width="300" height="200"><img src="{image}" \
#        width="300" height="200"</a>'.format(image=path)

        line = "\n\nSurface-based GLM results for {sbj} and {con}\n\n".format(
                sbj=sbj, con=con)
        content += line 
        tab =  "| Volume-based resample on fsaverage | Surface-based on fsaverage | Cluster for Surface-based on fsaverage |\n"
        tab += "| ---------------------------------- | -------------------------- | -------------------------------------- |\n"
        tab += "| {image1}     {image2}              | {image5}   {image6}        | {image9}       {image10}               |\n"
        tab += "| {image3}     {image4}              | {image7}   {image8}        | {image11}      {image12}               |\n".format(
                image1=paths_img_volume[0], image2=paths_img_volume[1], 
                image3=paths_img_volume[2], image4=paths_img_volume[3], 
                image5=paths_img_texture[0], image6=paths_img_texture[1],
                image7=paths_img_texture[2], image8=paths_img_texture[3],      
                image9=paths_img_texture_filter[0], image10=paths_img_texture_filter[1],
                image11=paths_img_texture_filter[2], image12=paths_img_texture_filter[3])
        
        content += tab

#Write the markdown file
file_summary = open(path_md, "w")
file_summary.write(content)
file_summary.close()

#Convert in html
cmd = "pandoc -s -S --toc {md} -o {output}".format(md=path_md, output=path_html)
os.system(cmd)