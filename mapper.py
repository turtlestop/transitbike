from flask import Flask, request, send_from_directory
from flask.json import jsonify
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from math import cos, asin, sqrt
import os, sys, time, polyline
import requests
import simplejson as json
from secret import APIKEY

nycsubs = [['W 4th St - Washington Sq (Lower)', 'B-D-F-M', [40.73225482650675, -74.0003081470682]], ['Buhre Ave', '6-6 Express', [40.846810332614844, -73.8325689992474]], ['51st St', '4-6-6 Express', [40.757107333148234, -73.971920000133]], ['86th St', '1-2', [40.78864433404891, -73.9762179981134]], ['Brooklyn Bridge - City Hall', '4-5-6-6 Express', [40.713065332984044, -74.0041310011169]], ['33rd St', '4-6-6 Express', [40.7460813321576, -73.9820760012492]], ['Lexington Ave - 59th St', '4-5-6-6 Express', [40.76252633389173, -73.9679670006644]], ['233rd St', '2-5', [40.89314357506239, -73.8573623943354]], ['66th St - Lincoln Ctr', '1-2', [40.773440334231445, -73.9822090004121]], ['Hunts Point Ave', '6-6 Express', [40.82094833186627, -73.8905489997538]], ['Canal St', '1-2', [40.722854331339036, -74.0062770002375]], ['Middletown Rd', '6-6 Express', [40.843863334673635, -73.8363219973265]], ['23rd St', '4-6-6 Express', [40.7398643335507, -73.9865990018397]], ['45th Rd - Court House Sq', '7-7 Express', [40.747023331863446, -73.9452640006533]], ['Astor Pl', '4-6-6 Express', [40.73005433376933, -73.991069998955]], ['59th St - Columbus Circle', '1-2', [40.76824733393756, -73.9819290016825]], ['Hunters Point Ave', '7-7 Express', [40.74221633326165, -73.94891600116]], ['96th St', '4-6-6 Express', [40.785672333485294, -73.9510700007068]], ['Mets - Willets Point', '7-7 Express', [40.75462233245772, -73.8456249978671]], ['23rd St', '1-2', [40.74408133288406, -73.9956570019647]], ['Houston St', '1-2', [40.72825133360782, -74.0053670018429]], ['3rd Ave - 138th St', '6-6 Express', [40.81047633454132, -73.9261380002227]], ['Zerega Ave', '6-6 Express', [40.83648833366287, -73.8470359980454]], ['104th St', 'A-S', [40.681711334202696, -73.837682999937]], ['Bleecker St (Downtown)', '4-6-6 Express', [40.72593123822929, -73.9946746782957]], ['Castle Hill Ave', '6-6 Express', [40.83425533183211, -73.8512219992089]], ['Broad Channel', 'A-S', [40.608402513981986, -73.8158326867774]], ['Ocean Pkwy', 'Q', [40.5763120005781, -73.968501000004]], ['50th St', '1-2', [40.76172833308103, -73.9838489999184]], ['Vernon Blvd - Jackson Ave', '7-7 Express', [40.74262633257131, -73.95358099882]], ['68th St - Hunter College', '4-6-6 Express', [40.768141333903976, -73.9638700014866]], ['Queensboro Plz', '7-7 Express-N-W', [40.75063598438094, -73.9401635343974]], ['Rockaway Blvd', 'A-S', [40.68042933335036, -73.843852997117]], ['Union Sq - 14th St', '4-5-6-6 Express', [40.734673334561, -73.9899509988698]], ['Junction Blvd', '7-7 Express', [40.74914533273112, -73.869526999796]], ['Classon Ave', 'G', [40.68888933367643, -73.9599900012695]], ['Bedford - Nostrand Aves', 'G', [40.68962733491343, -73.9535219998761]], ['15th St - Prospect Park', 'F-G', [40.660036021685464, -73.97973580607]], ['7th Ave', 'F-G', [40.666245023690635, -73.980251178869]], ['Ft Hamilton Pkwy', 'F-G', [40.65078200098824, -73.9757759988599]], ['Church Ave', 'F-G', [40.64427233346608, -73.9797211616719]], ['Beverly Rd', 'B-Q', [40.64390493165595, -73.964357795492]], ['Church Ave', 'B-Q', [40.6504935798757, -73.9628824614486]], ['Newkirk Ave', 'B-Q', [40.63514227039474, -73.9626948684797]], ['Parkside Ave', 'B-Q', [40.65507337471708, -73.9614534400078]], ['Prospect Park', 'B-Q-S', [40.66163378817137, -73.9620313045171]], ['Grand Army Plaza', '2-3-4', [40.67529502884244, -73.9709563314429]], ['Bergen St', '2-3-4', [40.68086247045291, -73.9749991509891]], ['Atlantic Ave', '2-3-4-5', [40.68442049853399, -73.9775499355033]], ['Rockaway Ave', 'A-C', [40.67834033324111, -73.9119459972731]], ['Fulton St', 'G', [40.687119332657794, -73.9753749987391]], ['Clinton - Washington Aves', 'G', [40.688094334588634, -73.9667959983086]], ['7th Ave', 'B-Q', [40.677102512887046, -73.9728527914631]], ['Atlantic Ave', 'B-Q', [40.68448865643635, -73.976783439311]], ['Union St', 'D-N-R', [40.67731600045995, -73.9831099993178]], ['Atlantic Av - Pacific St', 'D-N-R', [40.68366600047985, -73.978809999348]], ['Borough Hall', '4-5', [40.69240433310098, -73.9901510005831]], ['Aqueduct Racetrack (To Manh Only)', 'A', [40.672097332305505, -73.8359189987941]], ['DeKalb Ave', 'B-D-N-Q-R', [40.689804,-73.981164]], ['Morris Park', '5', [40.85436433270016, -73.860494999982]], ['Pelham Pkwy', '5', [40.8589853329393, -73.8553590000599]], ['Nostrand Ave', 'A-C', [40.68043833310734, -73.9504260004854]], ['Nevins St', '2-3-4-5', [40.68831091310594, -73.9804067986719]], ['Eastern Pkwy - Bklyn Museum', '2-3-4', [40.672032568925616, -73.9642220370174]], ['Franklin Ave', '2-3-4-5', [40.67076548645792, -73.9580997365901]], ['Beverly Rd', '2-5', [40.64512385265653, -73.9488479833557]], ['Church Ave', '2-5', [40.65086102070915, -73.9494551403219]], ['Newkirk Ave', '2-5', [40.63999157603046, -73.948299907532]], ['Brooklyn College - Flatbush Ave', '2-5', [40.63284274046751, -73.9475412071948]], ['Winthrop St', '2-5', [40.65665964750449, -73.950079345416]], ['Sterling St', '2-5', [40.66277332699014, -73.950728911504]], ['Crown Hts - Utica Ave', '3-4', [40.66897864436661, -73.9329325606634]], ['Kingston Ave', '3-4', [40.66948178160432, -73.942159783262]], ['Kingston - Throop Aves', 'A-C', [40.67991933291405, -73.9408589983912]], ['Nassau Ave', 'G', [40.72448033118355, -73.951182999797]], ['Greenpoint Ave', 'G', [40.73126733272315, -73.9544250017507]], ['Marcy Ave', 'J-M-Z', [40.7083833336101, -73.9578319999985]], ['Hewes St', 'J-M', [40.706890331217984, -73.9534880004084]], ['Essex St', 'J-M-Z', [40.718306389085505, -73.9874094023335]], ['138th St - Grand Concourse', '4-5', [40.81322433279863, -73.929848999481]], ['5th Ave - 53rd St', 'E-M', [40.76008716596106, -73.97524850466]], ['Lexington Ave - 53rd St', 'E-M', [40.75746864157252, -73.9690723741773]], ['28th St', 'N-R', [40.74545433330924, -73.9886980006626]], ['Herald Sq - 34th St', 'N-Q-R', [40.749644893078916, -73.987936833243]], ['1st Ave', 'L', [40.730975308760705, -73.9816808750905]], ['Grand Central - 42nd St', 'S', [40.75276900017257, -73.9791890000073]], ['Times Sq - 42nd St', 'S', [40.755983333482924, -73.986228999936]], ['42nd St - Bryant Pk', 'B-D-F-M', [40.75418433462967, -73.98459099839]], ['Times Sq - 42nd St', 'N-Q-R', [40.754612332230856, -73.98676800202]], ['Metropolitan Ave', 'G', [40.71277433427003, -73.9514239995614]], ['Grand St', 'L', [40.711576333817, -73.9404969989823]], ['Graham Ave', 'L', [40.71457633149971, -73.943943997881]], ['Lorimer St', 'L', [40.7140723341722, -73.9502480001933]], ['Bedford Ave', 'L', [40.71717433231373, -73.9566649983702]], ['Broadway', 'G', [40.70612690984066, -73.9503122559598]], ['Lorimer St', 'J-M', [40.70384433379361, -73.9473549981358]], ['Montrose Ave', 'L', [40.70739139725247, -73.9397928465133]], ['23rd St - Ely Av', 'E-M', [40.74776845479483, -73.946054702705]], ['Long Island City - Court Sq', 'G', [40.74630536706204, -73.9438155955715]], ['21st St', 'G', [40.74412900001313, -73.9495999993797]], ['39th Ave', 'N-Q', [40.752763394559445, -73.932851376069]], ['36th Ave', 'N-Q', [40.75644233343755, -73.9298619983323]], ['145th St', '1', [40.82655133277471, -73.950359998095]], ['157th St', '1', [40.83404133354386, -73.9448899987427]], ['96th St', '1-2-3', [40.79391933441861, -73.9723229994829]], ['103rd St', '1', [40.79944633394733, -73.9683789992482]], ['Central Park North (110th St)', '2-3', [40.79907533284112, -73.9518220010737]], ['103rd St', 'A-B-C', [40.79606107356255, -73.9613700821618]], ['Cathedral Pkwy (110th St)', 'A-B-C', [40.80058189158562, -73.9580667066434]], ['72nd St', '1-2-3', [40.77845333395168, -73.9819700010419]], ['72nd St', 'A-B-C', [40.77551973103465, -73.9763365754865]], ['81st St', 'A-B-C', [40.78134641772443, -73.9720979494142]], ['75th Ave', 'E-F', [40.71804498706881, -73.8369236931772]], ['Kew Gardens - Union Tpke', 'E-F', [40.714035152937456, -73.830370270175]], ['86th St', 'A-B-C', [40.785823379651546, -73.968828494562]], ['96th St', 'A-B-C', [40.79161913124813, -73.9646024565511]], ['Cathedral Pkwy (110th St)', '1', [40.803967333016914, -73.9668470001432]], ['116th St - Columbia University', '1', [40.807722334261875, -73.9641099979357]], ['125th St', '2-3', [40.807754332840474, -73.9454950001921]], ['135th St', '2-3', [40.81422933347776, -73.9407700002949]], ['149th St - Grand Concourse', '4', [40.81830377684673, -73.9273847543082]], ['116th St', '2-3', [40.80209833254597, -73.9496250010514]], ['Tremont Ave', 'B-D', [40.85041033318809, -73.9052270008801]], ['182nd-183rd Sts', 'B-D', [40.8560933318779, -73.9007409992674]], ['137th St - City College', '1', [40.82200833264513, -73.9536760003415]], ['145th St', '3', [40.82042133297881, -73.9362449989074]], ['176th St', '4', [40.84848033423412, -73.9117939980514]], ['Burnside Ave', '4', [40.853453334428735, -73.9076840006649]], ['170th St', 'B-D', [40.83930633332876, -73.9133999979605]], ['174th-175th Sts', 'B-D', [40.84590033357212, -73.9101360000397]], ['168th St', '1', [40.84055633285503, -73.940132998897]], ['181st St', '1', [40.849505333296115, -73.9335959998164]], ['168th St', 'A-C', [40.84071933346529, -73.9395609998789]], ['191st St', '1', [40.855225335009216, -73.929411997611]], ['175th St', 'A', [40.84739133395404, -73.9397039967383]], ['Beach 44th St', 'A', [40.59294333262581, -73.7760129988685]], ['Beach 60th St', 'A', [40.59237433461577, -73.7885219971778]], ['Beach 105th St', 'A-S', [40.583268770978755, -73.8275807493166]], ['Beach 98th St', 'A-S', [40.58538602425417, -73.8205205887206]], ['Rockaway Park - Beach 116 St', 'A-S', [40.58095619916644, -73.8355900859632]], ['Beach 90th St', 'A-S', [40.58809189768098, -73.8136514029455]], ['Beach 36th St', 'A', [40.59539833456184, -73.768174997928]], ['Beach 25th St', 'A', [40.60006633421964, -73.7613529967363]], ['Parsons Blvd', 'F', [40.70757233327444, -73.80328899878]], ['169th St', 'F', [40.71051783638578, -73.7934741978182]], ['103rd St - Corona Plaza', '7', [40.7498653343015, -73.862699997061]], ['111th St', '7', [40.751730332999585, -73.8553339972922]], ['63rd Dr - Rego Park', 'E-M-R', [40.72976430547176, -73.8616182002905]], ['Grant Ave', 'A-S', [40.67704433385241, -73.8650499980871]], ['79th St', '1-2', [40.78393433274081, -73.9799170004064]], ['Atlantic Ave', 'L', [40.675344999443105, -73.9030969991575]], ['Christopher St - Sheridan Sq', '1-2', [40.73342233397504, -74.00290599889]], ['E 149th St', '6', [40.812118331738084, -73.9040979979671]], ['Ozone Park - Lefferts Blvd', 'A-S', [40.68595133199964, -73.825797998395]], ['Times Sq - 42nd St', '7-7 Express', [40.75547733499068, -73.98769099766]], ['77th St', '4-6-6 Express', [40.77362033401498, -73.959873998072]], ['Woodside - 61st St', '7-7 Express', [40.74563033401391, -73.9029840008523]], ['111th St', 'A-S', [40.68433133342542, -73.8321629979318]], ['Flushing - Main St', '7-7 Express', [40.75960033237315, -73.8300300018334]], ['W 8th St - NY Aquarium', 'F-Q', [40.57603415120005, -73.9759578740407]], ['28th St', '1-2', [40.74721533235655, -73.9933650013927]], ['28th St', '4-6-6 Express', [40.74307033282793, -73.9842640014962]], ['Pelham Bay Park', '6-6 Express', [40.852462333145894, -73.8281209999571]], ['Westchester Sq - E Tremont Ave', '6-6 Express', [40.839892334397746, -73.842951998354]], ['18th St', '1-2', [40.741040332966726, -73.9978710011223]], ['Grand Central - 42nd St', '4-5-6-6 Express', [40.75180776311499, -73.9767132993616]], ['Grand Central - 42nd St', '7-7 Express', [40.75143133351694, -73.976041001197]], ['Canal St', '4-6-6 Express', [40.718803334727426, -74.0001929990035]], ['Beach 67th St', 'A', [40.590927334290434, -73.7969239989952]], ['W 4th St - Washington Sq (Upper)', 'A-C-E', [40.73233833138155, -74.0004950022554]], ['67th Ave', 'E-M-R', [40.72650580934677, -73.8528604836806]], ['85th St - Forest Pky', 'J', [40.692427333043625, -73.8600869993383]], ['Woodhaven Blvd', 'J-Z', [40.69370433254967, -73.852051996988]], ['111th St', 'J', [40.69711514442172, -73.8367933831]], ['121st St', 'J-Z', [40.70048233167487, -73.8283489992264]], ['Sutphin Blvd - Archer Av', 'E-J-Z', [40.70038275752361, -73.8080047191644]], ['Halsey St', 'L', [40.69551833448191, -73.9039340004711]], ['Myrtle Ave', 'L', [40.69947139533809, -73.9109757178021]], ['New Lots Ave', '3-4', [40.666315265574426, -73.884110707864]], ['Van Siclen Ave', '3-4', [40.66551829666946, -73.8894049162989]], ['Pennsylvania Ave', '3-4', [40.66471478435396, -73.8948859112423]], ['Van Siclen Ave', 'A-C', [40.67271033212401, -73.8903579997701]], ['Van Siclen Ave', 'J-Z', [40.67802854813373, -73.8916577259906]], ['Cleveland St', 'J', [40.679778332299975, -73.885194001242]], ['Livonia Ave', 'L', [40.664057604182275, -73.9005623715631]], ['Sutter Ave', 'L', [40.66914533375269, -73.9019159995943]], ['Junius St', '3-4', [40.66358933490929, -73.9024486409731]], ['Rockaway Ave', '3-4', [40.66261782103152, -73.908958335639]], ['Canarsie - Rockaway Pkwy', 'L', [40.64665400044553, -73.90184999993]], ['E 105th St', 'L', [40.650469118412055, -73.8995476931416]], ['Saratoga Ave', '3-4', [40.66153012321424, -73.9163302496604]], ['Sutter Ave - Rutland Road', '3-4', [40.664767122207614, -73.922521185067]], ['New Lots Ave', 'L', [40.65891510689037, -73.8992779601228]], ['Far Rockaway - Mott Ave', 'A', [40.60399533472034, -73.755404997895]], ['Chauncey St', 'J-Z', [40.682851634494526, -73.9103835693094]], ['Broadway Junction', 'J-Z', [40.679366334574624, -73.904289997425]], ['Halsey St', 'J', [40.68641560444364, -73.9166388839509]], ['Alabama Ave', 'J', [40.67699833360107, -73.8985260009904]], ['Shepherd Ave', 'A-C', [40.67413033485932, -73.8807499971029]], ['Norwood Ave', 'J-Z', [40.68152033389478, -73.8796259983382]], ['Crescent St', 'J-Z', [40.68315299047885, -73.873929251904]], ['Cypress Hills', 'J', [40.689616334196266, -73.8733219982875]], ['75th St - Eldert Ln', 'J-Z', [40.69129033462167, -73.867287998757]], ['69th St', '7', [40.746325332824334, -73.896402998386]], ['74th St - Broadway', '7', [40.746867907409886, -73.891205128382]], ['65th St', 'E-M-R', [40.74971986271151, -73.8987883776696]], ['Woodhaven Blvd - Queens Mall', 'E-M-R', [40.73309770715039, -73.869432084992]], ['Wyckoff Ave', 'M', [40.699454334648586, -73.9121789987563]], ['Seneca Ave', 'M', [40.70291933262727, -73.907581998429]], ['DeKalb Ave', 'L', [40.70369333256863, -73.9182320015304]], ['52nd St', '7', [40.7441493343501, -73.9125489981402]], ['46th St', 'E-M-R', [40.75631728599804, -73.9135217500592]], ['Northern Blvd', 'E-M-R', [40.75282516296223, -73.9060650802819]], ['46th St', '7', [40.74313233412849, -73.9184350005547]], ['82nd St - Jackson Hts', '7', [40.74765933320238, -73.8836969998634]], ['90th St - Elmhurst Av', '7', [40.748408334002924, -73.876612998942]], ['Grand Ave - Newtown', 'E-M-R', [40.73681375120887, -73.877220855937]], ['Elmhurst Ave', 'E-M-R', [40.74237041300368, -73.8820347458897]], ['Howard Beach - JFK Airport', 'A', [40.660476333123206, -73.8303009993043]], ['Aqueduct - North Conduit Av', 'A', [40.66823433458028, -73.8340579988262]], ['104th-102nd Sts', 'J-Z', [40.695166331888885, -73.8444349990019]], ['Briarwood - Van Wyck Blvd', 'E-F', [40.709162148863335, -73.820692635539]], ['Forest Hills - 71st Av', 'E-F-M-R', [40.72159464293687, -73.8445167192069]], ['Sutphin Blvd', 'F', [40.70541833253, -73.8108329982716]], ['Jamaica - Van Wyck', 'E', [40.70289888659826, -73.8170128702603]], ['Jamaica Ctr - Parsons / Archer', 'E-J-Z', [40.70206770924661, -73.8010963219811]], ['Simpson St', '2-5', [40.82397717486102, -73.8930663947183]], ['Freeman St', '2-5', [40.8299877799453, -73.8917522528532]], ['225th St', '2-5', [40.88802859157574, -73.8602146168679]], ['Elder Ave', '6', [40.82858433457284, -73.8791589978172]], ['Morrison Av - Soundview', '6', [40.829521335098256, -73.8745159988442]], ['Longwood Ave', '6', [40.81610433364345, -73.8964349986489]], ['Astoria Blvd', 'N-Q', [40.770037332517354, -73.9180950008212]], ['Astoria - Ditmars Blvd', 'N-Q', [40.7750359996785, -73.912034000185]], ['Jackson Ave', '2-5', [40.816437799808796, -73.9077019385347]], ['Prospect Ave', '2-5', [40.81948759780675, -73.901777786243]], ['Cypress Ave', '6', [40.80536833435186, -73.9140419994168]], ['Whitlock Ave', '6', [40.82652533380191, -73.8862829983243]], ['Intervale Ave', '2-5', [40.82214246442492, -73.896617383584]], ['174th St', '2-5', [40.837195883313186, -73.8876935975168]], ['Pelham Pkwy', '2-5', [40.85719274250162, -73.8674806776188]], ['Allerton Ave', '2-5', [40.86548371157605, -73.8672342277634]], ["E 143rd St - St Mary's St", '6', [40.808719334136455, -73.9076569988394]], ['Kingsbridge Rd', '4', [40.867760333744734, -73.8971740010191]], ['Bedford Park Blvd - Lehman College', '4', [40.8734123326929, -73.8900640005615]], ['Harlem - 148 St', '3', [40.82388033407589, -73.9364699999187]], ['Mt Eden Ave', '4', [40.844434333833284, -73.9146849986492]], ['Fordham Rd', 'B-D', [40.86129633182038, -73.8977490007685]], ['170th St', '4', [40.84007533283499, -73.9177909970935]], ['Kingsbridge Rd', 'B-D', [40.86697833331913, -73.8935090000309]], ['Bedford Park Blvd', 'B-D', [40.87324433171974, -73.8871379986991]], ['Marble Hill - 225th St', '1', [40.87456133275337, -73.9098309989177]], ['231st St', '1', [40.87885633187432, -73.9048340004263]], ['215th St', '1', [40.869444332904905, -73.9152789993084]], ['207th St', '1', [40.864614333714016, -73.9188190007204]], ['Inwood - 207th St', 'A', [40.8680723332653, -73.9198990007626]], ['238th St', '1', [40.884667334326366, -73.9008699993626]], ['Van Cortlandt Park - 242nd St', '1', [40.88924833345021, -73.8985829997981]], ['West Farms Sq - E Tremont Av', '2-5', [40.84020796544077, -73.8799612780955]], ['St Lawrence Ave', '6', [40.83150933406975, -73.867617998263]], ['Bronx Park East', '2-5', [40.848768999811156, -73.868356091237]], ['Gun Hill Rd', '2-5', [40.87783971871569, -73.8661341042237]], ['219th St', '2-5', [40.88388830753444, -73.86250970748]], ['Mosholu Pkwy', '4', [40.87975033296914, -73.8846549998888]], ['Norwood - 205th St', 'D', [40.874811333682345, -73.8788549984991]], ['Burke Ave', '2-5', [40.87125913561442, -73.8670536167708]], ['Baychester Ave', '5', [40.87866333374528, -73.8385909977719]], ['Eastchester - Dyre Ave', '5', [40.88830033249039, -73.8308340008274]], ['Jamaica - 179th St', 'F', [40.712645999940975, -73.7838170004415]], ['Wakefield - 241st St', '2', [40.90312533408352, -73.8506199983527]], ['Botanic Garden', 'S', [40.670342999976114, -73.9592449997529]], ['Bushwick - Aberdeen', 'L', [40.682860958491204, -73.9052617622733]], ['Wilson Ave', 'L', [40.68886687533081, -73.9039586049314]], ['Broadway Junction', 'L', [40.67845658203403, -73.9031175784343]], ['Gun Hill Rd', '5', [40.86952633288799, -73.8463840010297]], ['E 180th St', '2-5', [40.84186337449904, -73.87334609435]], ['Dyckman St', '1', [40.86053133457367, -73.925535999775]], ['125th St', '1', [40.8155813329265, -73.9583720009297]], ['Park Pl', 'S', [40.674771999887255, -73.957624000331]], ['Franklin Ave - Fulton St', 'S', [40.68059599942808, -73.9558270010879]], ['Nereid Ave (238 St)', '2-5', [40.898286849118136, -73.8543153099791]], ['149th St - Grand Concourse', '2-5', [40.81833047711118, -73.926722474577]], ['3rd Ave - 149th St', '2-5', [40.816029585709344, -73.9177915270379]], ['161st St - Yankee Stadium', '4', [40.82823066063588, -73.925691994952]], ['167th St', '4', [40.83553733302143, -73.9213999975664]], ['Brook Ave', '6', [40.80756633325041, -73.919239998173]], ['33rd St', '7', [40.744587333592726, -73.9309969987384]], ['40th St', '7', [40.743781334697424, -73.924015998061]], ['145th St', 'A-B-C-D', [40.82476669406457, -73.9440879283577]], ['155th St', 'B-D', [40.83013533321578, -73.9382089980995]], ['161st St - Yankee Stadium', 'B-D', [40.82790533241327, -73.9256509975147]], ['167th St', 'B-D', [40.83376933205918, -73.9184320007708]], ['Ralph Ave', 'A-C', [40.678822334523645, -73.9207859991904]], ['Utica Ave', 'A-C', [40.67936433301651, -73.9307289984532]], ['36th St', 'E-M-R', [40.751960377482355, -73.9290181847038]], ['Steinway St', 'E-M-R', [40.756987692724486, -73.9205264710409]], ['Kosciuszko St', 'J', [40.69317233423697, -73.9285089985691]], ['Gates Ave', 'J-Z', [40.68958433256818, -73.922156000587]], ['Central Ave', 'M', [40.69787333339047, -73.927242998295]], ['Knickerbocker Ave', 'M', [40.698660334772896, -73.9197200009711]], ['Broadway', 'N-Q', [40.761432332024945, -73.9258229985642]], ['30th Ave', 'N-Q', [40.76677899973269, -73.9214790000599]], ['Jefferson St', 'L', [40.706606999359956, -73.9229129995305]], ['Morgan Ave', 'L', [40.70615200009972, -73.9331469999883]], ['Queens Plz', 'E-M-R', [40.748918053128584, -73.93713823926]], ['18th Ave', 'F', [40.62975500011662, -73.9769709998775]], ['Ditmas Ave', 'F', [40.63611899980037, -73.978171999927]], ['77th St', 'R', [40.62974200015178, -74.0255099995847]], ['Bay Ridge Ave', 'R', [40.63496700028034, -74.02337699924]], ['55th St', 'D', [40.631479094385625, -73.9953488255311]], ['50th St', 'D', [40.636261224383965, -73.9946587800965]], ['Ft Hamilton Pkwy', 'N', [40.631386000144154, -74.0053510007241]], ['8th Ave', 'N', [40.63497133283626, -74.0115159973591]], ['25th Ave', 'D', [40.59770400016762, -73.986829000164]], ['Bay Pky', 'D', [40.601950795212716, -73.99367619974]], ['20th Ave', 'N', [40.61710933301559, -73.9845219984124]], ['18th Ave', 'N', [40.620687331248675, -73.9904539985985]], ['Bay Ridge - 95th St', 'R', [40.6166220006113, -74.03087600063]], ['86th St', 'R', [40.62268700032295, -74.028398000283]], ['79th St', 'D', [40.613159259344464, -74.00058287394]], ['71st St', 'D', [40.61925904300817, -73.998840949054]], ['20th Ave', 'D', [40.604677331055306, -73.9981743210267]], ['18th Ave', 'D', [40.607736065209444, -74.0015925925407]], ['62nd St', 'D', [40.626224796104694, -73.9968572505166]], ['New Utrecht Ave', 'N', [40.624842000193794, -73.9963530004669]], ['Ave U', 'F', [40.595925159151875, -73.9733764190409]], ['Kings Hwy', 'F', [40.60325873883345, -73.9723553083373]], ['Brighton Beach', 'B-Q', [40.57771052976751, -73.9613537857206]], ['Sheepshead Bay', 'B-Q', [40.58654788005143, -73.9540579118221]], ['Ave U', 'B-Q', [40.5993092845579, -73.95581122321]], ['Kings Hwy', 'B-Q', [40.608638978424565, -73.9576087353908]], ['Ave U', 'N', [40.59723633364408, -73.9790840008704]], ['Kings Hwy', 'N', [40.60405933336751, -73.9803730021255]], ['Neptune Ave', 'F', [40.58073909152164, -73.9745927280223]], ['Ave X', 'F', [40.589449999847005, -73.9742659993022]], ['Bay 50th St', 'D', [40.588840999864985, -73.9837650002573]], ['Gravesend - 86th St', 'N', [40.592465333902624, -73.9781889997666]], ['Ave P', 'F', [40.60884314257858, -73.973002815289]], ['Ave N', 'F', [40.61435704529457, -73.9740485090751]], ['Bay Pky', 'F', [40.62073195620631, -73.9752569775524]], ['Ave M', 'B-Q', [40.61739807818342, -73.9592431047764]], ['Bay Pky', 'N', [40.61145612298434, -73.9817800102403]], ['Ave I', 'F', [40.625017773484714, -73.9760693319356]], ['Ave J', 'B-Q', [40.625023152905705, -73.9606931624677]], ['Ave H', 'B-Q', [40.62920871052413, -73.9615179387401]], ['Neck Rd', 'B-Q', [40.59532202457638, -73.9550782744625]], ['21st St - Queensbridge', 'F', [40.75373960398463, -73.9419376138154]], ['50th St', 'A-C-E', [40.762456332634045, -73.9859839999905]], ['7th Ave', 'B-D-E', [40.76297048549053, -73.9816978238128]], ['47th-50th Sts - Rockefeller Ctr', 'B-D-F-M', [40.75864133466554, -73.981331002119]], ['57th St', 'F', [40.76408533390238, -73.9773680013077]], ['Lexington Ave - 63rd St', 'F', [40.764618428150776, -73.9660896434021]], ['Roosevelt Island - Main St', 'F', [40.75917233330991, -73.9532350000272]], ['59th St - Columbus Circle', 'A-B-C-D', [40.768249864983254, -73.9816487233667]], ['49th St', 'N-Q-R', [40.75980230703365, -73.9842095658089]], ['57th St', 'N-Q-R', [40.76456585850871, -73.980729733136]], ['5th Ave - 59th St', 'N-Q-R', [40.76481133275182, -73.973347000184]], ['Lexington Ave - 59th St', 'N-Q-R', [40.762709188743855, -73.967375016644]], ['34th St - Penn Station', '1-2-3', [40.75037333357704, -73.9910569993341]], ['Times Sq - 42nd St', '1-2-3', [40.75529033316711, -73.9874950004336]], ['Broadway - Nassau St', 'A-C', [40.71016249872167, -74.0076230934279]], ['Chambers St', 'A-C', [40.714111334148996, -74.008584736068]], ['42nd St - Port Authority Bus Term', 'A-C-E', [40.75730833180808, -73.9897350004381]], ['Myrtle-Willoughby Aves', 'G', [40.69461933256742, -73.9490669982815]], ['Flushing Ave', 'G', [40.70037699951844, -73.950234000506]], ['23rd St', 'F-M', [40.74295465088764, -73.9927650045465]], ['Herald Sq - 34th St', 'B-D-F-M', [40.74978973294837, -73.9877718901554]], ['Hoyt - Schermerhorn Sts', 'A-C-G', [40.68840880947581, -73.985036239956]], ['Jay St - Borough Hall', 'A-C-F', [40.69247097044472, -73.9872181531118]], ['East Broadway', 'F', [40.71385533408638, -73.9901770011736]], ['Delancey St', 'F', [40.718681075658196, -73.988078068379]], ['Lower East Side - 2nd Ave', 'F', [40.7234019995008, -73.9899379994914]], ['Flushing Ave', 'J-M', [40.70040473673457, -73.9413773482563]], ['Myrtle Ave', 'J-M-Z', [40.69719533361235, -73.9356230004067]], ['4th Ave', 'F-G', [40.67027200058139, -73.9897789996763]], ['Smith - 9th Sts', 'F-G', [40.673641394609135, -73.9958917275746]], ['Bergen St', 'F-G', [40.68611088098272, -73.9907564955075]], ['Lawrence St', 'N-R', [40.69225572936931, -73.9860566782987]], ['Court St', 'N-R', [40.694196814120716, -73.9918183091348]], ['Union Sq - 14th St', 'N-Q-R', [40.73587260060109, -73.990538861684]], ['23rd St', 'N-R', [40.74130300016866, -73.9893440004543]], ['Prospect Ave', 'D-N-R', [40.665414000093335, -73.9928720005896]], ['9th St', 'D-N-R', [40.67084700022307, -73.9883019997]], ['3rd Ave', 'L', [40.73269133261918, -73.9857500009869]], ['Union Sq - 14th St', 'L', [40.73476364552659, -73.9906697694308]], ['Liberty Ave', 'A-C', [40.67454233286892, -73.8965480007524]], ['Broadway Junction', 'A-C', [40.67833399982758, -73.905316000291]], ['59th St', 'N-R', [40.64136199944241, -74.0178809996847]], ['45th St', 'N-R', [40.648938999878794, -74.0100060003595]], ['36th St', 'D-N-R', [40.655143999751665, -74.0035489995692]], ['9th Ave', 'D', [40.64648441084645, -73.9944487440854]], ['53rd St', 'N-R', [40.645069000509004, -74.0140340004904]], ['Ft Hamilton Pkwy', 'D', [40.64091304459246, -73.9942022375282]], ['25th St', 'D-N-R', [40.66039700032125, -73.9980909998328]], ['Carroll St', 'F-G', [40.68027368469693, -73.9949469798202]], ['Spring St', 'A-C-E', [40.7262273349522, -74.003738998729]], ['181st St', 'A', [40.85169533266245, -73.9379690016355]], ['190th St', 'A', [40.859022332220405, -73.9341799993755]], ['116th St', 'A-B-C', [40.805058467107635, -73.9547977809277]], ['125th St', 'A-B-C-D', [40.81107200632826, -73.9522479975436]], ['Prince St', 'N-R', [40.72432899922576, -73.9977020000719]], ['8th St - NYU', 'N-R', [40.730465331990395, -73.992507998909]], ['Fulton St', '2-3', [40.70941633229353, -74.0065710002491]], ['Park Pl', '2-3', [40.713051332200514, -74.0088109998716]], ['Chambers St', '1-2-3', [40.71547833317367, -74.0092660017244]], ['Hoyt St', '2-3', [40.69054451845209, -73.9850637961165]], ['Borough Hall', '2-3', [40.69321933265995, -73.9899979990653]], ['183rd St', '4', [40.85840733349188, -73.903879000705]], ['Fordham Rd', '4', [40.86280333320703, -73.9010339983319]], ['World Trade Center', 'E', [40.71256426010712, -74.0097446147848]], ['Canal St - Holland Tunnel', 'A-C-E', [40.72082433307871, -74.0052290019119]], ['155th St', 'A-C', [40.83051833300836, -73.9415140002858]], ['163rd St - Amsterdam Av', 'A-C', [40.836013332605724, -73.9398920015931]], ['Fulton St', 'J-Z', [40.71002299961088, -74.007938000877]], ['Chambers St', 'J-Z', [40.7132341227328, -74.00340673089]], ['Canal St', 'J-Z', [40.71817420996139, -73.9998263855514]], ['City Hall', 'N-R', [40.713272664531246, -74.0069858179477]], ['Canal St', 'N-R', [40.71946533477728, -74.0018259997318]], ['South Ferry', '1', [40.70173084095291, -74.0131689598393]], ['Bowling Green', '4-5', [40.70491433249645, -74.0140079984819]], ['Wall St', '4-5', [40.707557334362484, -74.0118619992053]], ['Whitehall St', 'N-R', [40.70314270735986, -74.0130072373643]], ['Rector St', 'N-R', [40.70774508995048, -74.0129745623741]], ['Fresh Pond Rd', 'M', [40.70622633198259, -73.8958980008641]], ['Middle Village - Metropolitan Ave', 'M', [40.71143163827924, -73.8895772297876]], ['Rector St', '1', [40.70751333304196, -74.0137830008063]], ['Cortlandt St (Temporarily Closed)', '1', [40.71183533452517, -74.0121880006975]], ['Fulton St', '4-5', [40.71036833193085, -74.009508998743]], ['Broad St', 'J-Z', [40.70647633411761, -74.0110560004892]], ['Cortlandt St (NB only)', 'N-R', [40.710513317670305, -74.011131964839]], ['Wall St', '2-3', [40.70682133279038, -74.0090999989945]], ['Dyckman St', 'A', [40.86549133254293, -73.9272709991317]], ['Grand St', 'B-D', [40.71826733292375, -73.9937529992589]], ['Broadway - Lafayette St', 'B-D-F-M', [40.725297332299235, -73.9962039984028]], ['Bowery', 'J-Z', [40.72024721673806, -73.9938069067281]], ['Canal St', 'N-Q', [40.71881459682263, -74.0010547125305]], ['23rd St', 'A-C-E', [40.745906332964005, -73.9980410006117]], ['34th St - Penn Station', 'A-C-E', [40.752287334131175, -73.9933909993041]], ['Jackson Hts - Roosevelt Av', 'E-F-M-R', [40.74654002448512, -73.8912986649895]], ['14th St', '1-2-3', [40.737826333308426, -74.0002010005942]], ['135th St', 'A-B-C', [40.817905892108634, -73.947534808324]], ['14th St', 'F-M', [40.73822833288366, -73.9962089989117]], ['6th Ave', 'L', [40.737741803112115, -73.9977507887229]], ['8th Ave', 'L', [40.73977700012131, -74.002578000477]], ['14th St', 'A-C-E', [40.74089333363853, -74.0016899994375]], ['Nostrand Ave', '3-4', [40.66993848398767, -73.9504262489382]], ['Clark St', '2-3', [40.69746633298482, -73.9930859983266]], ['Franklin Ave', 'A-C', [40.6813799997593, -73.9568479998051]], ['Clinton - Washington Aves', 'A-C', [40.683263332875605, -73.9658379986855]], ['Forest Ave', 'M', [40.70441233402832, -73.9030749999464]], ['110th St', '4-6-6 Express', [40.79502033352402, -73.9442499969671]], ['86th St', '4-5-6-6 Express', [40.77949233177087, -73.9555889997845]], ['York St', 'F', [40.69974300092185, -73.9868849998245]], ['High St', 'A-C', [40.69933733273785, -73.9905310009556]], ['Lafayette Ave', 'A-C', [40.686113333301115, -73.9739459982416]], ['President St', '2-5', [40.667883936572196, -73.9505892005588]], ['Woodlawn', '4', [40.88603733314497, -73.8787509989088]], ['Bleecker St (Uptown)', '4-6-6 Express', [40.72591499972982, -73.9946590001332]], ['103rd St', '4-6-6 Express', [40.790600332975615, -73.9474780015154]], ['Euclid Ave', 'A-C-S', [40.67537733193324, -73.872105999942]], ['88th St', 'A-S', [40.67984333439131, -73.851469998935]], ['Cortelyou Rd', 'B-Q', [40.640940498719964, -73.9637900549486]], ['116th St', '4-6-6 Express', [40.79862933384588, -73.941616998284]], ['Parkchester', '6-6 Express', [40.83322633218034, -73.860815999958]], ['Franklin St', '1-2', [40.71931833420651, -74.0068860022655]], ['80th St', 'A-S', [40.679371334570604, -73.8589920012129]], ['5th Ave - Bryant Pk', '7-7 Express', [40.75382133359373, -73.9819629987137]], ['Spring St', '4-6-6 Express', [40.72230133331719, -73.9971409995061]], ['125th St', '4-5-6-6 Express', [40.804138334029325, -73.9375940001906]], ['Coney Island - Stillwell Av', 'D-F-N-Q', [40.57728133344397, -73.9812359985597]]]

def directions (origin, destination, mode):
    base_url = 'https://maps.googleapis.com/maps/api/directions/json'
    geo = {
        'origin': origin,
        'destination': destination,
        'mode': mode,
        'key': APIKEY}
    if mode == 'transit':
        geo['time'] = ninish
    r = requests.get(base_url, params=geo)
    response = r.json()
    route = response['routes'][0]
    legs = route['legs'][0]
    return dict(route=route,legs=legs)

def distancematrix (origins, dests, mode):
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    print('origins: %s ' %origins)
    print('dests: %s ' %dests)
    geo = {
        'origins': origins,
        'destinations': dests,
        'mode': mode,
        'key': APIKEY}
    if mode == 'transit':
        geo['time'] = ninish
    r = requests.get(base_url, params=geo)
    response = r.json()
    print(response)
    if len(response['destination_addresses'])>1:
        times = [time['duration']['value'] for time in response['rows'][0]['elements']]
    else:
        times = [time['elements'][0]['duration']['value'] for time in response['rows']]
    print(times)
    #relying on the fact that google returns times in the same order as dests:
    return times

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods
        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp
            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp
        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
app = Flask(__name__)

def geocode(address):
    base_url = 'http://maps.googleapis.com/maps/api/geocode/json'
    geo = {'address': address}
    r = requests.get(base_url, params=geo)
    response = r.json()
    return response['results'][0]['geometry']['location']

def distance(lat1, lon1, lat2, lon2):
    # a bit overkill, but a quick way getting pretty accurate distances between lat and long coords using trig
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

# sbdata.txt contains lat/long info for all nyc subways
subwaykeys = ['name', 'line', 'geo', 'dist']

# given orig and dest, returns all subways less than 1/2 dist from orig to dest(to avoid making api
# calls for every station)
def nearbysubs_variant(orig, dest):
    subways = nycsubs[:]
    subway_with_dists = [subway + [distance(orig['lat'], orig['lng'], subway[2][0], subway[2][1])] for subway in subways]
    nearest_subways = sorted(subway_with_dists, key = lambda x: x[-1])[:20]
    cutoff = distance(orig['lat'], orig['lng'], dest['lat'], dest['lng'])
    nearby_subways = filter(lambda x: x[-1]<cutoff, nearest_subways)
    subway_dicts = [dict(zip(subwaykeys, subway)) for subway in nearby_subways]
    return subway_dicts

def nearbysubs(orig, dest):
    cutoff = distance(orig['lat'],orig['lng'], dest['lat'], dest['lng'])/2
    listofstations = []
    for subway in nycsubs:
        subwaydist = distance(orig['lat'], orig['lng'], subway[2][0], subway[2][1])
        if subwaydist > cutoff:
            continue
        subway.append(subwaydist)
        listofstations.append(dict(zip(subwaykeys, subway)))
    sortedlist = sorted(listofstations, key = lambda x: x['dist'])[:30]
    return sortedlist


def ppformat(lst):
    return [{'lat': i[0], 'lng': i[1]} for i in lst]

# for mode=transit, googlemaps directions api accepts a time. For realistic morning commute times, going to force 9am.
ninish = int(time.mktime(time.struct_time([2016,7,14,9,30,0,0,0,0])))

home = '191 5th avenue, brooklyn, new york'
recurse = '455 broadway, new york'

@app.route("/route", methods=["POST", "GET"])
@crossdomain(origin='*')
def router ():
    form_origin = request.form.get("str1")
    form_dest = request.form.get("str2")
    transit_data = biketransit(form_origin, form_dest)
    return jsonify(transit_data)

def fastestmatrix (origin, destination):
    orig_geo = geocode(origin)
    dest_geo = geocode(destination)
    bikeopts = nearbysubs(orig_geo,dest_geo)
    candidatesubs = '|'.join([str(station['geo'][0]) + ',' + str(station['geo'][1]) for station in bikeopts])
    biketimes = distancematrix(origin, candidatesubs, 'bicycling')
    subwaytimes = distancematrix(candidatesubs, destination, 'transit')
    for subway, bike_time, sub_time in zip(bikeopts, biketimes, subwaytimes):
        subway['totaltime'] = bike_time + sub_time
    return sorted(bikeopts, key = lambda x: x['totaltime'])[0]


def gettraveltime (dirs):
    return dirs['legs']['duration']['value']/60

def getoverviewpline (dirs):
    return ppformat(polyline.decode(dirs['route']['overview_polyline']['points']))

def subway_router (origin, destination):
    subway_directions = directions(origin, destination, 'transit')
    time = gettraveltime(subway_directions)
    details = {'time': time}
    legs = []
    for step in subway_directions['legs']['steps']:
        stage = {}
        if 'transit_details' in step:
            stage['type'] = 'subway'
            stage['line'] = step['transit_details']['line']['short_name']
            stage['color'] = step['transit_details']['line']['color']
            stage['pline'] = ppformat(polyline.decode(step['polyline']['points']))
        else:
            stage['type'] = 'walking'
            stage['pline'] = ppformat(polyline.decode(step['polyline']['points']))
        legs.append(stage)
    details['legs'] = legs
    return details

def geotostring (geolist):
    geostr = str(geolist[0]) + ',' + str(geolist[1])
    return geostr

def mixed_modal_router (origin, destination):
    # calculates the fastest bike+subway route from origin to destination
    fastest_combo = fastestmatrix(origin, destination)
    mid_sub_name = fastest_combo['name']
    midway_subway = geotostring(fastest_combo['geo'])
    bike_leg = bike_router(origin, midway_subway)
    subway_leg = subway_router(midway_subway, destination)
    mixed_route = dict(mid_sub_name=mid_sub_name, bike_leg=bike_leg, subway_leg=subway_leg)
    return mixed_route

def bike_router(origin, destination):
    # gets pline and time to bike from origin, destination
    all_bike_route = directions(origin, destination, 'bicycling')
    bike_time = gettraveltime(all_bike_route)
    bike_pline = getoverviewpline(all_bike_route)
    bike_details = {'time': bike_time, 'pline': bike_pline}
    return bike_details

def str_to_lst(str):
    lat = str.split(',')[0]
    lng = str.split(',')[1]
    return [lat,lng]

def biketransit (origin, destination):
    # calculates and returns best all bike, all transit, and mixed routes
    time_to_beat = gettraveltime(directions(origin, destination, 'transit'))
    bike_details = bike_router(origin, destination)
    mixed_modal_route = mixed_modal_router(origin, destination)
    results = dict(time_to_beat=time_to_beat, bike_details=bike_details, mixed_modal_route=mixed_modal_route)
    return results

@app.route("/jtest", methods=["POST", "GET"])
@crossdomain(origin='*')
def jtest():
    dta = [0, [[{"lat": 40.67684, "lng": -73.98017}, {"lat": 40.68021, "lng": -73.97789}, {"lat": 40.68085, "lng": -73.97745}, {"lat": 40.68149, "lng": -73.97703}, {"lat": 40.68246, "lng": -73.97954}, {"lat": 40.68344, "lng": -73.97887}, {"lat": 40.68364, "lng": -73.97874}], [{"lat": 40.68367, "lng": -73.97881}, {"lat": 40.68473, "lng": -73.97812}, {"lat": 40.6849, "lng": -73.97804}, {"lat": 40.68507, "lng": -73.97799}, {"lat": 40.68524, "lng": -73.97798}, {"lat": 40.68759, "lng": -73.97834}, {"lat": 40.68777, "lng": -73.97844}, {"lat": 40.68793, "lng": -73.97859}, {"lat": 40.68807, "lng": -73.9788}, {"lat": 40.68883, "lng": -73.98068}, {"lat": 40.68899, "lng": -73.9809}, {"lat": 40.68918, "lng": -73.98108}, {"lat": 40.6894, "lng": -73.98121}, {"lat": 40.69156, "lng": -73.9823}, {"lat": 40.69383, "lng": -73.98343}, {"lat": 40.69508, "lng": -73.98413}, {"lat": 40.69777, "lng": -73.98548}, {"lat": 40.71488, "lng": -73.99501}, {"lat": 40.71497, "lng": -73.99506}, {"lat": 40.71515, "lng": -73.99517}, {"lat": 40.71533, "lng": -73.9953}, {"lat": 40.71608, "lng": -73.99603}, {"lat": 40.71621, "lng": -73.99619}, {"lat": 40.71632, "lng": -73.99639}, {"lat": 40.71642, "lng": -73.99661}, {"lat": 40.71701, "lng": -73.99832}, {"lat": 40.71725, "lng": -73.99885}, {"lat": 40.71739, "lng": -73.99909}, {"lat": 40.71838, "lng": -74.00046}, {"lat": 40.71855, "lng": -74.00044}, {"lat": 40.71868, "lng": -74.00033}, {"lat": 40.71917, "lng": -73.99987}, {"lat": 40.71953, "lng": -74.00064}, {"lat": 40.71991, "lng": -74.00146}, {"lat": 40.72016, "lng": -74.00124}, {"lat": 40.72063, "lng": -74.00084}]], [[{"lat": 40.67684, "lng": -73.98017}, {"lat": 40.68021, "lng": -73.97789}, {"lat": 40.68211, "lng": -73.97659}, {"lat": 40.68236, "lng": -73.97642}, {"lat": 40.68241, "lng": -73.97637}, {"lat": 40.68246, "lng": -73.97629}, {"lat": 40.68311, "lng": -73.97676}, {"lat": 40.68421, "lng": -73.97756}, {"lat": 40.68433, "lng": -73.97765}, {"lat": 40.68439, "lng": -73.97752}], [{"lat": 40.68445, "lng": -73.97757}, {"lat": 40.68439, "lng": -73.97769}, {"lat": 40.68459, "lng": -73.97783}, {"lat": 40.6847, "lng": -73.97791}, {"lat": 40.68492, "lng": -73.97807}, {"lat": 40.68509, "lng": -73.97795}, {"lat": 40.68511, "lng": -73.97778}, {"lat": 40.68513, "lng": -73.97761}, {"lat": 40.68522, "lng": -73.97763}, {"lat": 40.68445, "lng": -73.978}, {"lat": 40.68458, "lng": -73.97691}, {"lat": 40.68723, "lng": -73.97742}, {"lat": 40.68732, "lng": -73.97745}, {"lat": 40.68747, "lng": -73.97755}, {"lat": 40.6876, "lng": -73.97771}, {"lat": 40.6877, "lng": -73.97793}, {"lat": 40.68873, "lng": -73.98047}, {"lat": 40.68879, "lng": -73.98061}, {"lat": 40.68894, "lng": -73.98085}, {"lat": 40.68913, "lng": -73.98104}, {"lat": 40.68934, "lng": -73.98118}, {"lat": 40.69156, "lng": -73.9823}, {"lat": 40.69383, "lng": -73.98343}, {"lat": 40.69508, "lng": -73.98413}, {"lat": 40.69777, "lng": -73.98548}, {"lat": 40.71488, "lng": -73.99501}, {"lat": 40.71497, "lng": -73.99506}, {"lat": 40.71506, "lng": -73.99511}, {"lat": 40.71524, "lng": -73.99523}, {"lat": 40.71541, "lng": -73.99538}, {"lat": 40.71615, "lng": -73.99611}, {"lat": 40.71627, "lng": -73.99629}, {"lat": 40.71637, "lng": -73.9965}, {"lat": 40.71706, "lng": -73.99846}, {"lat": 40.71732, "lng": -73.99897}, {"lat": 40.71838, "lng": -74.00046}, {"lat": 40.71855, "lng": -74.00044}, {"lat": 40.71868, "lng": -74.00033}, {"lat": 40.71917, "lng": -73.99987}, {"lat": 40.71953, "lng": -74.00064}, {"lat": 40.71991, "lng": -74.00146}, {"lat": 40.72016, "lng": -74.00124}, {"lat": 40.72063, "lng": -74.00084}]]]
    lst = [{'lat': 4, 'lng': 6}]
    lst2 = json.dumps(dta)
    return lst2

@app.route("/")
def send_foo():
     return send_from_directory('static', 'mapper.html')


@app.route("/toy", methods=["POST", "GET"])
@crossdomain(origin='*')
def toyfunction():
    str1 = request.form.get("str1")
    str2 = request.form.get("str2")
    if request.method == 'POST':
        return "You made a POST %s request with the inputs str1: %s; str2: %s \n" %(doubletext(top), str1, str2)
    else:
        return "You made a GET request with the input: %s \n" %(str1)
#
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
