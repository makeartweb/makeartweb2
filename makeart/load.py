
def main(root):
    from makeart import models
    
    from transaction import commit
    import os
    
    models.add_content(root, models.ModelWood(), 'mymodel')
    
    for item in ['fernanda', 'te', 'amo']:
        models.add_content(root['mymodel'], models.ItemModelWood(), item)
    
    #models.add_content(root,  models.Folding(), 'fonts')
    #
    #for filefont in os.listdir('./makeart/fonts'):
    #    models.add_content(root['fonts'],
    #                       models.Font(os.path.join('./makeart/fonts', filefont)) ,
    #                       '-'.join(filefont.split('.')[:-1]))
    #
    ##root['pdf1']['0'].set_thumbnail(root['pdf0'].pdfmodel.get_path())
    #
    ##root['pdf1']['1'].set_thumbnail(root['pdf0'].pdfmodel.get_path())
    #
    ##root['pdf0'].[].set_mask(root['pdf0'].pdfmodel.get_path())
    #
    commit()