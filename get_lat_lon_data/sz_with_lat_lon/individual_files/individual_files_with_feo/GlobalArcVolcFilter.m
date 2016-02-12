function FinalArcOut=GlobalArcVolcFilter(ArcName, MyHeaders, AddColumns, Type)
%Input arc data must be GeoRocDownload, check all boxes for metadata out.
%Type 1=6 vals, Type 2 = Mg#55 vals, Type3=Mg#>60 Vals, Type 4= Raw
%Add two initial columns (1s column and volcano name column)
%Headers must have major elements bound by SiO2 and LOI, 
%U(PPM) must be last TE column, currently HF176_HF177 must be last iso col


%Addcolumns line here for reference
% AddColumns=[{'Mg#'} {'Eu/Eu*'} {'Eu/Eu**'} {'ASI'} {'Dy/Yb'} {'Li/Y'} {'Zr/Nb'} {'Nb/Ta'} {'Rb/Nb'} {'Ba/Nb'} {'Rb/Cs'} {'Nb/Zr'} {'Pb/Nb'} {'Cs/Nb'} {'La/Nb'}...
%     {'La/Zr'} {'Th/Nb'} {'Th/Zr'} {'La/Yb'} {'La/Sm'} {'Pb/Ce'} {'Pb/La'} {'Ba/La'} {'Sm/La'} {'Th/La'} {'Zr/Sm'} {'Zr/Hf'} {'Zr/Ti'} {'Sr/Nd'} {'Sm/Nd'} {'Th/U'} {'Gd/Yb'} {'Sr/Zr'}];

NumCols=size(MyHeaders,2);
SampCol=find(strcmpi(MyHeaders(1,:),'SAMPLE NAME'));
YearCol=find(strcmpi(MyHeaders(1,:),'Year'));
VolcanoCol=find(strcmpi(MyHeaders(1,:),'Volcano'));
AltCol=find(strcmpi(MyHeaders(1,:),'ALTERATION'));
LocCol=find(strcmpi(MyHeaders(1,:),'LOCATION'));
LocComCol=find(strcmpi(MyHeaders(1,:),'LOCATION COMMENT'));
MethodCol=find(strcmpi(MyHeaders(1,:),'METHOD'));
SiO2Col=find(strcmpi(MyHeaders(1,:),'SIO2(WT%)'));
MgOCol=find(strcmpi(MyHeaders(1,:),'MGO(WT%)'));
Fe2O3Col=find(strcmpi(MyHeaders(1,:),'FE2O3(WT%)'));
Fe2O3TCol=find(strcmpi(MyHeaders(1,:),'FE2O3T(WT%)'));
FeOCol=find(strcmpi(MyHeaders(1,:),'FEO(WT%)'));
FeOTCol=find(strcmpi(MyHeaders(1,:),'FEOT(WT%)'));
Al2O3Col=find(strcmpi(MyHeaders(1,:),'AL2O3(WT%)'));
Na2OCol=find(strcmpi(MyHeaders(1,:),'NA2O(WT%)'));
CaOCol=find(strcmpi(MyHeaders(1,:),'CAO(WT%)'));
K2OCol=find(strcmpi(MyHeaders(1,:),'K2O(WT%)'));
LOICol=find(strcmpi(MyHeaders(1,:),'LOI(WT%)'));
NbCol=find(strcmpi(MyHeaders(1,:),'NB(PPM)'));
TaCol=find(strcmpi(MyHeaders(1,:),'TA(PPM)'));
LiCol=find(strcmpi(MyHeaders(1,:),'LI(PPM)'));
YCol=find(strcmpi(MyHeaders(1,:),'Y(PPM)'));
SmCol=find(strcmpi(MyHeaders(1,:),'SM(PPM)')); 
EuCol=find(strcmpi(MyHeaders(1,:),'EU(PPM)'));
GdCol=find(strcmpi(MyHeaders(1,:),'GD(PPM)'));
TbCol=find(strcmpi(MyHeaders(1,:),'TB(PPM)'));
UCol=find(strcmpi(MyHeaders(1,:),'U(PPM)')); 
DyCol=find(strcmpi(MyHeaders(1,:),'DY(PPM)'));
YbCol=find(strcmpi(MyHeaders(1,:),'YB(PPM)')); 
ZrCol=find(strcmpi(MyHeaders(1,:),'ZR(PPM)'));
RbCol=find(strcmpi(MyHeaders(1,:),'RB(PPM)'));
BaCol=find(strcmpi(MyHeaders(1,:),'BA(PPM)'));
CsCol=find(strcmpi(MyHeaders(1,:),'CS(PPM)')); 
PbCol=find(strcmpi(MyHeaders(1,:),'PB(PPM)'));
LaCol=find(strcmpi(MyHeaders(1,:),'LA(PPM)'));
ThCol=find(strcmpi(MyHeaders(1,:),'TH(PPM)'));
CeCol=find(strcmpi(MyHeaders(1,:),'CE(PPM)'));
HfCol=find(strcmpi(MyHeaders(1,:),'HF(PPM)')); 
TiCol=find(strcmpi(MyHeaders(1,:),'TIO2(WT%)'));
SrCol=find(strcmpi(MyHeaders(1,:),'SR(PPM)'));
NdCol=find(strcmpi(MyHeaders(1,:),'ND(PPM)')); 


LastCol=find(strcmpi(MyHeaders(1,:),'HF176_HF177'));
[Arc_num,Arc_txt,Arc_FullDat] = xlsread([ArcName '.xls']);
SmChon=0.153;
EuChon=0.0583;
GdChon=0.2055;
TbChon=0.0374;

TE1Cols=[find(strcmpi(MyHeaders(1,:),'SC(PPM)'))... %TE allowed for emissions techniques
    find(strcmpi(MyHeaders(1,:),'V(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'CR(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'MN(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'CO(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'NI(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'CU(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'ZN(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'GA(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'GE(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'RB(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'SR(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'Y(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'ZR(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'SC(PPM)'))...
    find(strcmpi(MyHeaders(1,:),'BA(PPM)'))];
TE2Cols=setdiff((LOICol+1):UCol,TE1Cols);

%Selectable filtering criteria
if Type < 4
MinYear=1975;
MinMg=4;
MaxMg=12;
MinEuEuStar=0.85;
MaxEuEuStar=1.15;
MinLOI=2;
end
% % Below for NO FILTER
% if Type == 4
% MinYear=1975;
% MinMg=0;
% MaxMg=16;
% MinEuEuStar=0;
% MaxEuEuStar=2;
% MinLOI=4;
% end
%Below for "Raw" Values
if Type == 4
MinYear=1975;
MinMg=4;
MaxMg=16;
MinEuEuStar=0;
MaxEuEuStar=2;
MinLOI=2;
end
%Fill GeoRoc data into MyHeaders format
FormattedArc=cell(size(Arc_FullDat,1),NumCols);
for i=1:NumCols
    for j=1:size(Arc_FullDat,2)
        if strcmpi(MyHeaders(i),Arc_FullDat(1,j))
            FormattedArc(:,i)=Arc_FullDat(:,j);
        end
    end
end

%Deactivate Data from earlier than MinYear, extensively altered, or LOI>2
for i=2:length(FormattedArc(:,1))
    if FormattedArc{i,YearCol}<MinYear
        Arc_num(i-1,1)=0;
    end
    if strcmpi(FormattedArc{i,AltCol},'EXTENSIVELY ALTERED')
        Arc_num(i-1,1)=0;
    end
    if FormattedArc{i,LOICol}>MinLOI
        Arc_num(i-1,1)=0;
    end
end

%Recompile Active Rows - Filter step 1 removes rows designated as not
%Young (<~200,000yr), not on the arc front, or not a long lived stratocone (Selected by hand in primary data files), as well as data
%from before the date designated above
ArcFilter1=cell(sum(Arc_num(:,1))+1,NumCols);
ArcFilter1(1,:)=MyHeaders;
j=1;
for i=2:length(FormattedArc(:,1))
    if Arc_num(i-1,1)
        j=j+1;
        ArcFilter1(j,:)=FormattedArc(i,:);
    end
end



%Compile samples to single rows, each with a section for 'All
%Data','ICPMS or better only'.  For Majors XRF>WET>AES>AAS>OTHER. 
%First major elements
StillIn=ones(size(ArcFilter1,1),1);
MEDataType=ones(size(ArcFilter1,1),1);
for i=2:size(ArcFilter1,1)
    MEDataType(i)=0;
    if isempty(strfind(ArcFilter1{i,MethodCol},'EMP'))==0
        MEDataType(i)=1;
    elseif strcmpi(ArcFilter1(i,MethodCol),'AAS')
        MEDataType(i)=2;
    elseif strcmpi(ArcFilter1(i,MethodCol),'AES')
        MEDataType(i)=3;
    elseif strcmpi(ArcFilter1(i,MethodCol),'WET')
        MEDataType(i)=4;
    elseif strcmpi(ArcFilter1(i,MethodCol),'XRF')
        MEDataType(i)=5;
    end
end
TEDataType1=ones(size(ArcFilter1,1),1); %Order of methods for TE measureable by emission/flourescence
for i=2:size(ArcFilter1,1)
    TEDataType1(i)=0;
    if (isempty(strfind(ArcFilter1{i,MethodCol},'NAA'))==0) || strcmpi(ArcName,'Colombia and Ecuador') %Allow inferior data for Columbia/Ecuador
        TEDataType1(i)=1;
    elseif isempty(strfind(ArcFilter1{i,MethodCol},'AES'))==0
        TEDataType1(i)=2;
    elseif isempty(strfind(ArcFilter1{i,MethodCol},'XRF'))==0
        TEDataType1(i)=3;
    elseif isempty(strfind(ArcFilter1{i,MethodCol},'MS'))==0
        TEDataType1(i)=4;
    end
end
TEDataType2=ones(size(ArcFilter1,1),1); %Order of methods for other TE
for i=2:size(ArcFilter1,1)
    TEDataType2(i)=0;
    if (isempty(strfind(ArcFilter1{i,MethodCol},'DCPAES'))==0) || (strcmpi(ArcName,'Colombia and Ecuador') && isempty(strfind(ArcFilter1{i,MethodCol},'ICPAES'))==0)
        TEDataType2(i)=1;
    elseif isempty(strfind(ArcFilter1{i,MethodCol},'NAA'))==0
        TEDataType2(i)=2;
    elseif isempty(strfind(ArcFilter1{i,MethodCol},'MS'))==0
        TEDataType2(i)=3;
    end
end
%In order to determine which analyses are of the same sample, it is
%necessary to match sample name, Location, and Location comment.  This is
%due to non-unique sample name entries in GeoRoc
LocComNaNs=zeros(length(ArcFilter1(:,1)),1);
for i=1:length(ArcFilter1(:,1))
    LocComNaNs(i)=sum(isnan(ArcFilter1{i,LocComCol}));
end
LocComNaNIdx=find(LocComNaNs);    
CompRow=1;
CompArctemp=cell(size(ArcFilter1));
CompArctemp(1,:)=MyHeaders;
%for i=9:9
for i=2:size(ArcFilter1,1)
    if StillIn(i)==1
        CompRow=CompRow+1;
        clear SampIdxA
        clear SampIdxB
        clear SampIdxC
        clear SampIdx
        clear SampVals
        SampIdxA=find(strcmpi(ArcFilter1(i,SampCol),ArcFilter1(:,SampCol))); %Locate indices of sample name matches
        SampIdxB=find(strcmpi(ArcFilter1(i,LocCol),ArcFilter1(:,LocCol))); %Locate indices of location matches
        if sum(isnan(ArcFilter1{i,LocComCol})) %Locate indices of location comment matches (if present)
            SampIdxC=LocComNaNIdx;
        else
            SampIdxC=find(strcmpi(ArcFilter1(i,LocComCol),ArcFilter1(:,LocComCol))); 
        end
        SampIdx=intersect(intersect(SampIdxA,SampIdxB),SampIdxC); %Index name+loc+comment matches
        SampVals=cell(length(SampIdx),NumCols+4);
        for j=1:length(SampIdx)
            SampVals(j,:)=[ArcFilter1(SampIdx(j),:) MEDataType(SampIdx(j)) ArcFilter1((SampIdx(j)),YearCol) TEDataType1(SampIdx(j)) TEDataType2(SampIdx(j))];
            StillIn(SampIdx(j))=0;
        end
        
        %Insert MEs
        SortedSampValsME=flipdim(sortrows(SampVals,[NumCols+1, NumCols+2]),1); %matrix of sample analyses, sorted by ME preference, then year (best on top)
        CompArctemp(CompRow,1:SiO2Col-1)=SortedSampValsME(1,1:SiO2Col-1);
        %if length(SampIdx)>0
            for j=1:size(SortedSampValsME,1)
                for k=SiO2Col:LOICol
                    if (isempty(CompArctemp{CompRow,k}) || sum(isnan(CompArctemp{CompRow,k}))>0) %If the cell hasn't been filled yet (empty or NaN), 
                        if isempty(SortedSampValsME{j,k})==0 && SortedSampValsME{j,k}>0 %and the new value is >0 
                            CompArctemp(CompRow,k)=SortedSampValsME(j,k); %fill in new value
                        end
                    end
                end
            end
        %end            
        %Insert TE1s
        SortedSampValsTE1=flipdim(sortrows(SampVals,[NumCols+3, NumCols+2]),1);
        if SortedSampValsTE1{1,NumCols+3}>0
            for j=1:size(SortedSampValsTE1,1)
                if SortedSampValsTE1{j,NumCols+3}>0
                    for k=1:length(TE1Cols)
                        if (isempty(CompArctemp{CompRow,TE1Cols(k)}) || sum(isnan(CompArctemp{CompRow,TE1Cols(k)}))>0)
                            if isempty(SortedSampValsTE1{j,TE1Cols(k)})==0 && SortedSampValsTE1{j,TE1Cols(k)}>0
                                CompArctemp(CompRow,TE1Cols(k))=SortedSampValsTE1(j,TE1Cols(k));
                            end
                        end
                    end
                end
            end
        end
        %Insert TE2s
        SortedSampValsTE2=flipdim(sortrows(SampVals,[NumCols+4, NumCols+2]),1);
        if SortedSampValsTE2{1,NumCols+4}>0
            for j=1:size(SortedSampValsTE2,1)
                if SortedSampValsTE2{j,NumCols+4}>0
                    for k=1:length(TE2Cols)
                        if (isempty(CompArctemp{CompRow,TE2Cols(k)}) || sum(isnan(CompArctemp{CompRow,TE2Cols(k)}))>0)
                            if isempty(SortedSampValsTE2{j,TE2Cols(k)})==0 && SortedSampValsTE2{j,TE2Cols(k)}>0
                                CompArctemp(CompRow,TE2Cols(k))=SortedSampValsTE2(j,TE2Cols(k));
                                if TE2Cols(k)==NbCol %if inserting into Nb column
                                    if SortedSampValsTE2{j,NumCols+4}==1 %if method is DCPAES
                                        CompArctemp{CompRow,TE2Cols(k)}=[]; %set Nb col to nothing
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end
        %Insert ISOs
        SortedSampValsISO=flipdim(sortrows(SampVals,NumCols+2),1); %rank iso analyses by date only
        
        for j=1:size(SortedSampValsISO,1)
            for k=(UCol+1):LastCol
                if isempty(CompArctemp{CompRow,k}) || sum(isnan(CompArctemp{CompRow,k}))>0
                    CompArctemp(CompRow,k)=SortedSampValsISO(j,k);
                end
            end
        end
    end   
end
CompArc=CompArctemp(1:CompRow,1:NumCols);
FinalArcFilt=cell(length(CompArc(:,1)),NumCols+size(AddColumns,2));
FinalArcFilt(1,:)=[MyHeaders(1:LastCol) AddColumns MyHeaders(LastCol+1:end)];
EuEuStar=cell(length(CompArc(:,1)),1);
EuEuStarStar=cell(length(CompArc(:,1)),1);
FinalRow=1;
%AddColumns=[{'Mg#'} {'Eu/Eu*'} {'Eu/Eu**'} ASI {'Dy/Yb'} {'Li/Y'} {'Zr/Nb'} {'Nb/Ta'} {'Rb/Nb'}  {'Ba/Nb'} {'Rb/Cs'} {'Nb/Zr'} {'Pb/Nb'} {'Cs/Nb'} {'La/Nb'}...
%    {'La/Zr'} {'Th/Nb'} {'Th/Zr'} {'La/Yb'} {'La/Sm'} {'Pb/Ce'} {'Pb/La'} {'Ba/La'} {'Sm/La'} {'Th/La'} {'Zr/Sm'} {'Zr/Hf'} {'Zr/Ti'} {'Sr/Nd'} {'Sm/Nd'} {'Th/U'} {'Gd/Yb'} {'Sr/Zr'}];  
CompArc(cellfun(@isempty,CompArc)) = {NaN};%Replace empty cells with NaN for simplicity

%Calculate FeOT where absent
for i=2:size(CompArc,1)
    if isnan(CompArc{i,FeOTCol})
        if isnan(CompArc{i,Fe2O3TCol})
            Fe2O3asFeO=nansum([0; CompArc{i,Fe2O3Col}])*.899;
            NewFeOT=nansum([Fe2O3asFeO; CompArc{i,FeOCol}]);
            if NewFeOT>0
                CompArc{i,FeOTCol}=NewFeOT;
            end
        else
            NewFeOT=CompArc{i,Fe2O3TCol}*.899;
            if NewFeOT>0
                CompArc{i,FeOTCol}=CompArc{i,Fe2O3TCol}*.899;
            end
        end
    end
end
    
    
for i=2:size(CompArc,1) %apply final filtering step here
    EuEuStar{i,1}=(CompArc{i,EuCol}/EuChon)/mean([CompArc{i,SmCol}/SmChon CompArc{i,GdCol}/GdChon]);
    EuEuStarStar{i,1}=(CompArc{i,EuCol}/EuChon)/((CompArc{i,SmCol}/SmChon)*(2/3)+(CompArc{i,TbCol}/TbChon)*(1/3));
    if (isempty(CompArc{i,MgOCol})+sum(isnan(CompArc{i,MgOCol})))==0 && ((isempty(EuEuStar{i})+sum(isnan(EuEuStar{i})))==0 || (isempty(EuEuStarStar{i})+sum(isnan(EuEuStarStar{i})))==0) %must have Mg and either Eu/Eu* or Eu/Eu**
        if CompArc{i,MgOCol}>=MinMg && CompArc{i,MgOCol}<=MaxMg  %Mg filter
            %below if statement: if EuStar requirement is met OR EuStar is
            %NaN and the EuStarStar requirement is met instead
            if (EuEuStar{i}>=MinEuEuStar && EuEuStar{i}<=MaxEuEuStar) || (isnan(EuEuStar{i}) && (EuEuStarStar{i}>=MinEuEuStar && EuEuStarStar{i}<=MaxEuEuStar))  %must meet cut offs for Eu/Eu* and Mg
                FinalRow=FinalRow+1;
                ASI=(CompArc{i,Al2O3Col}/101.96)/((CompArc{i,CaOCol}/56.08)+(CompArc{i,Na2OCol}/61.98)+(CompArc{i,K2OCol}/94.2));
                MgNum=(CompArc{i,MgOCol}/40.3)/((CompArc{i,MgOCol}/40.3)+(CompArc{i,FeOTCol}/71.84));
                FinalArcFilt(FinalRow,1:LastCol+size(AddColumns,2))=[ArcName CompArc(i,2:LastCol) MgNum EuEuStar(i) EuEuStarStar(i) ASI CompArc{i,DyCol}/CompArc{i,YbCol}  CompArc{i,LiCol}/CompArc{i,YCol} CompArc{i,ZrCol}/CompArc{i,NbCol} CompArc{i,NbCol}/CompArc{i,TaCol}...
                    CompArc{i,RbCol}/CompArc{i,NbCol} CompArc{i,BaCol}/CompArc{i,NbCol} CompArc{i,RbCol}/CompArc{i,CsCol} CompArc{i,NbCol}/CompArc{i,ZrCol}...
                    CompArc{i,PbCol}/CompArc{i,NbCol} CompArc{i,CsCol}/CompArc{i,NbCol} CompArc{i,LaCol}/CompArc{i,NbCol} CompArc{i,LaCol}/CompArc{i,ZrCol}...
                    CompArc{i,ThCol}/CompArc{i,NbCol} CompArc{i,ThCol}/CompArc{i,ZrCol} CompArc{i,LaCol}/CompArc{i,YbCol} CompArc{i,LaCol}/CompArc{i,SmCol} CompArc{i,PbCol}/CompArc{i,CeCol}...
                    CompArc{i,PbCol}/CompArc{i,LaCol} CompArc{i,BaCol}/CompArc{i,LaCol} CompArc{i,SmCol}/CompArc{i,LaCol}  CompArc{i,ThCol}/CompArc{i,LaCol} CompArc{i,ZrCol}/CompArc{i,SmCol}...
                    CompArc{i,ZrCol}/CompArc{i,HfCol} CompArc{i,ZrCol}/CompArc{i,TiCol} CompArc{i,SrCol}/CompArc{i,NdCol} CompArc{i,SmCol}/CompArc{i,NdCol} CompArc{i,ThCol}/CompArc{i,UCol}...
                    CompArc{i,GdCol}/CompArc{i,YbCol} CompArc{i,SrCol}/CompArc{i,ZrCol}];%<--- add functions here
                if Type == 1
                if CompArc{i,MgOCol}>=5.5 && CompArc{i,MgOCol}<=6.5 %Fill in columns to be averaged for 6 values
                    FinalArcFilt(FinalRow,LastCol+size(AddColumns,2)+1:end)=CompArc(i,SiO2Col:UCol);
                end
                end
                if Type == 2
                if MgNum>=.50 && MgNum<=.60 %Fill in columns to be averaged for Mg#55 values
                    FinalArcFilt(FinalRow,LastCol+size(AddColumns,2)+1:end)=CompArc(i,SiO2Col:UCol);
                end
                end
                if Type == 3
                if MgNum>=.60 %Fill in columns to be averaged for Mg#>60 values
                    FinalArcFilt(FinalRow,LastCol+size(AddColumns,2)+1:end)=CompArc(i,SiO2Col:UCol);
                end
                end
                if Type == 4
                    FinalArcFilt(FinalRow,LastCol+size(AddColumns,2)+1:end)=CompArc(i,SiO2Col:UCol);
                end
            end
        end
    end
end
FinalArcOut=FinalArcFilt(1:FinalRow,:);
FinalArcOut(2:end,:)=sortcell(FinalArcFilt(2:FinalRow,:),[VolcanoCol LocCol]);
    
    