""" types of the output packets (last digit of the pack name) """

TYPES = dict(
    app=0, # ambulance
    dsc=2, # day stacionar
    onk=3, # oncology
    sto=5, # stomatology
    pcr=7, # PCR tests # COVID-19 file, not used
    ifa=8, # IFA tests # COVID-19 file, not used
    tra=9, # travmatology
    xml=0 # default
)


